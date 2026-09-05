"""QueryNest — AI chat and search routes."""
from flask import Blueprint, request, jsonify, session
from datetime import datetime
import re
import database as db_module
from utils.helpers import normalize_query, detect_language, is_hindi_query, translate_hindi_to_english
from utils.ai_client import call_claude_ai, save_ai_answer, is_programming_topic
from utils.search import search_local_json, search_db

ai_bp = Blueprint('ai', __name__)

def _save_history(user_id, query, language, source):
    users = db_module.get_users()
    if users is None or not user_id: return
    try:
        entry = {'query': query, 'language': language or '', 'source': source,
                 'searched_at': datetime.now().isoformat()}
        users.update_one({'user_id': user_id},
            {'$push': {'search_history': {'$each': [entry], '$slice': -50}},
             '$inc':  {'total_searches': 1},
             '$set':  {'last_search': datetime.now().isoformat()}})
    except Exception as e:
        print(f"History update error: {e}")


# ── /api/search ───────────────────────────────────────────────────
@ai_bp.route('/api/search', methods=['POST'])
def smart_search():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    data        = request.get_json() or {}
    query       = data.get('query', '').strip()
    use_ai      = data.get('use_ai', False)
    forced_lang = data.get('lang', '').strip().lower()
    limit       = int(data.get('limit', 1))
    user_id     = session['user_id']

    if not query:
        return jsonify({'success': False, 'message': 'Empty query'})

    if is_hindi_query(query):
        query = translate_hindi_to_english(query)

    norm     = normalize_query(query)
    det_lang = forced_lang if forced_lang in ['sql','mysql','mongodb','python','java','c','cpp'] \
               else detect_language(norm)

    if not forced_lang and not is_programming_topic(norm):
        return jsonify({
            'success': False, 'source': 'out_of_scope',
            'message': '❌ **QueryNest sirf programming aur database queries ke liye hai!**\n\n'
                       '✅ Try: `prime number python`, `fibonacci c`, `create table students`'
        })

    if limit > 1:
        json_results = search_local_json(query, forced_lang=det_lang)
        if not json_results:
            json_results = search_local_json(det_lang or query, forced_lang=det_lang)
        return jsonify({'success': True, 'source': 'local_json',
                        'results': json_results[:limit]})

    if not use_ai:
        lang_hint = det_lang or 'python'
        db         = db_module.get_db()
        db_results = search_db(db, query, forced_lang=det_lang)
        if db_results:
            best      = db_results[0]
            lang_used = best.get('language', lang_hint)
            _save_history(user_id, query, lang_used, 'database')
            return jsonify({'success': True, 'source': 'database',
                            'result': {'title': best.get('title', query),
                                       'content': best.get('content', ''),
                                       'language': lang_used}})

        json_results = search_local_json(query, forced_lang=det_lang)
        if json_results:
            best = json_results[0]
            _save_history(user_id, query, best.get('language') or lang_hint, 'local_json')
            return jsonify({'success': True, 'source': 'local_json',
                            'result': {'title': best.get('title', query),
                                       'content': best.get('content', ''),
                                       'language': best.get('language', lang_hint)}})

        _save_history(user_id, query, lang_hint, 'not_found')
        return jsonify({
            'success': False,
            'source':  'not_found',
            'query':   query,
            'lang':    lang_hint,
            'message': f'**"{query}"** ka jawab abhi available nahi hai.\n\n'
                       '🤖 AI se poochho — fresh accurate answer milega!'
        })

    lang_hint       = det_lang or 'python'
    ai_text, ai_err = call_claude_ai(query, lang_hint)
    if ai_text:
        db = db_module.get_db()
        save_ai_answer(db, query, ai_text, lang_hint, 'claude_ai')
        _save_history(user_id, query, lang_hint, 'claude_ai')
        return jsonify({'success': True, 'source': 'ai',
                        'result': {'title': query, 'content': ai_text, 'language': lang_hint}})

    import config as _cfg
    raw_key = getattr(_cfg, 'GROQ_API_KEY', '').strip()
    has_key = bool(raw_key) and 'YOUR' not in raw_key and raw_key.startswith('gsk_')

    if has_key:
        msg = f'⚠️ AI response nahi aaya — network issue ya rate limit.\n**Error:** `{ai_err}`\n\nThodi der baad try karo.'
    else:
        msg = ('🔑 **Groq API key set nahi hai!** `config.py` mein `GROQ_API_KEY` daalo.\n\n'
               '**FREE key lo:** https://console.groq.com → Sign up → API Keys\n\n'
               'Key set karne ke baad server restart karo — phir AI kaam karega! 🚀')

    return jsonify({'success': False, 'source': 'no_key', 'message': msg})


# ── /api/anthropic  AND  /api/gemini-chat ────────────────────────
@ai_bp.route('/api/gemini-chat', methods=['POST'])
@ai_bp.route('/api/anthropic', methods=['POST'])
def ai_chat():
    """Unified AI chat — smart offline fallback."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.get_json() or {}

    simple_message = data.get('message', '').strip()
    simple_lang    = data.get('lang', '').strip().lower()
    sys_raw        = data.get('system', '')

    conv_msgs = data.get('messages', [])
    if not conv_msgs and simple_message:
        conv_msgs = [{'role': 'user', 'content': simple_message}]

    message = ''
    for msg in reversed(conv_msgs):
        if msg.get('role') == 'user':
            message = msg.get('content', '').strip()
            break
    if not message:
        message = simple_message

    lang_map = {'cpp': 'cpp', 'c++': 'cpp', 'java': 'java', 'python': 'python',
                'sql': 'sql', 'mysql': 'mysql', 'mongodb': 'mongodb', 'c': 'c'}
    if simple_lang and simple_lang in lang_map:
        eff_lang = lang_map[simple_lang]
    else:
        lang_match = re.search(r'Active Language[:\s]+([A-Za-z+]+)', sys_raw, re.IGNORECASE)
        eff_lang = lang_map.get(lang_match.group(1).lower(), 'python') if lang_match else \
                   (detect_language(message.lower()) or 'python')

    DB_LANGS = {'sql', 'mysql', 'mongodb'}
    PROG_KEYWORDS = [
        'armstrong', 'fibonacci', 'factorial', 'palindrome', 'prime',
        'bubble sort', 'insertion sort', 'selection sort', 'binary search',
        'linked list', 'stack', 'queue', 'recursion', 'class', 'inheritance',
        'swap', 'reverse', 'pattern', 'star', 'triangle', 'matrix',
        'whole number', 'natural number', 'digit', 'calculator', 'harshad',
        'happy number', 'perfect number', 'anagram', 'gcd', 'lcm',
        'array', 'sorting', 'searching', 'even', 'odd', 'number series',
    ]
    SQL_KEYWORDS = [
        'create table', 'drop table', 'alter table', 'select ', 'insert into',
        'update set', 'delete from', 'primary key', 'foreign key', 'join ',
        'group by', 'order by', 'where ', 'having ', 'index', 'constraint',
    ]
    MONGO_KEYWORDS = [
        'db.', 'find(', 'aggregate(', 'insertone', 'insertmany', 'updateone',
        'deleteone', 'collection', 'mongodb', 'nosql', 'mongoose',
    ]
    msg_lower = message.lower()
    # Step 1: message clearly has SQL keywords — force sql regardless of tab
    if any(kw in msg_lower for kw in SQL_KEYWORDS):
        eff_lang = 'mysql' if 'mysql' in msg_lower else 'sql'
    # Step 2: message clearly has MongoDB keywords — force mongodb
    elif any(kw in msg_lower for kw in MONGO_KEYWORDS):
        eff_lang = 'mongodb'
    # Step 3: DB tab selected but message looks like programming query
    elif eff_lang in DB_LANGS:
        detected = detect_language(msg_lower)
        if detected and detected not in DB_LANGS:
            eff_lang = detected
        elif any(kw in msg_lower for kw in PROG_KEYWORDS):
            eff_lang = 'python'

    if not message:
        msg = '⚠️ Empty message received.'
        return jsonify({'reply': msg, 'content': [{'type': 'text', 'text': msg}]})

    if is_hindi_query(message):
        message = translate_hindi_to_english(message)

    # ── Non-programming check: friendly rejection ─────────────────
    NON_PROG_KEYWORDS = [
        'recipe', 'meggi', 'maggi', 'khana', 'food', 'cook', 'weather',
        'cricket', 'movie', 'film', 'song', 'celebrity', 'politics',
        'election', 'news', 'love', 'relationship', 'joke', 'story',
        'poem', 'essay', 'history', 'geography'
    ]
    msg_lower = message.lower()
    if any(kw in msg_lower for kw in NON_PROG_KEYWORDS):
        reply = (
            "😄 Yaar, main **programming AI** hoon — Maggi banana nahi jaanta! 🍜\n\n"
            "Main sirf **code aur database** ke sawaalon mein help kar sakta hoon:\n\n"
            "✅ **Try karo:**\n"
            "- `fibonacci series java`\n"
            "- `create table students sql`\n"
            "- `bubble sort python`\n"
            "- `armstrong number c++`\n\n"
            "Koi programming sawaal poochho — main poora code likhke dunga! 🚀"
        )
        return jsonify({'reply': reply, 'content': [{'type': 'text', 'text': reply}]})

    lang_name = eff_lang.upper()

    system_prompt = (
        f"You are QueryNest AI — a smart, friendly programming assistant.\n"
        f"Current language focus: {lang_name}.\n"
        "BEHAVIOR:\n"
        f"1) Write code ONLY in {lang_name} unless user explicitly asks for another language\n"
        "2) Give COMPLETE, WORKING, RUNNABLE code — no '...' or placeholder comments\n"
        "3) Add a short inline comment on important lines\n"
        "4) Wrap ALL code in triple backticks with the language label\n"
        "5) After the code, show expected output as a comment block\n"
        "6) Respond in Hinglish (Hindi + English mix) — friendly and conversational tone\n"
        "7) Be helpful and thorough — explain HOW the code works in 2-3 sentences\n"
        "8) NEVER say 'I cannot help' for programming questions — always answer\n"
        "9) For multi-step problems, break down the logic before the code"
    )

    trimmed_msgs = conv_msgs[-6:] if conv_msgs else [{'role': 'user', 'content': message}]

    # ── Try real AI first ────────────────────────────────────────
    ai_text, ai_err = call_claude_ai(message, eff_lang,
                                     system_prompt=system_prompt,
                                     messages=trimmed_msgs)
    if ai_text:
        db = db_module.get_db()
        save_ai_answer(db, message, ai_text, eff_lang, 'claude_ai')
        return jsonify({
            'success': True,
            'reply':   ai_text,
            'content': [{'type': 'text', 'text': ai_text}]
        })

    # ── AI failed — show honest error, no fake built-in fallback ──
    print(f"[AI Chat] AI unavailable ({ai_err})")

    import config as _cfg
    raw_key = getattr(_cfg, 'GROQ_API_KEY', '').strip()
    has_key = bool(raw_key) and 'YOUR' not in raw_key and raw_key.startswith('gsk_')

    if has_key:
        no_answer = (
            f"⚠️ **AI response nahi aaya** — network issue ya rate limit ho sakta hai.\n\n"
            f"**Error:** `{ai_err}`\n\n"
            f"Thodi der baad dobara try karo."
        )
    else:
        no_answer = (
            f"🔑 **Groq API key set nahi hai!**\n\n"
            f"`config.py` mein apni FREE Groq key daalo:\n"
            f"```\nGROQ_API_KEY = 'gsk_xxxxxxxxxxxxxxxxxxxx'\n```\n\n"
            f"FREE key yahan se lo: https://console.groq.com\n"
            f"(Sign up → API Keys → Create API Key)\n\n"
            f"Key set karne ke baad server restart karo — phir AI kaam karega! 🚀"
        )
    return jsonify({
        'success': False,
        'source': 'no_key',
        'reply':   no_answer,
        'content': [{'type': 'text', 'text': no_answer}]
    })


# ── /api/execute ─────────────────────────────────────────────────
@ai_bp.route('/api/execute', methods=['POST'])
def execute_code():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.get_json() or {}
    code = data.get('code', '').strip()
    lang = data.get('lang', 'python').lower()
    stdin_data = data.get('stdin', None)  # User-provided stdin input
    if not code:
        return jsonify({'output': '⚠ Empty code', 'error': True})
    from utils.code_runner import run_code
    result = run_code(code, lang, stdin_data=stdin_data)
    return jsonify({'success': True, **result})
