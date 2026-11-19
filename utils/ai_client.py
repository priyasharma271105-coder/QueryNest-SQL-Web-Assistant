"""QueryNest — AI client powered by Groq (FREE).
Uses the official `groq` Python package to avoid Cloudflare 403 blocks
that occur with raw urllib requests.

Get your FREE key at: https://console.groq.com  (sign up → API Keys → Create)
Install package:      pip install groq
"""
import os
import config
from utils.helpers import normalize_query, detect_language

# ── Topic keyword lists ───────────────────────────────────────────────────────
DB_TOPIC_KEYWORDS = [
    'select','insert','update','delete','create','drop','alter','table','join',
    'where','group by','order by','index','view','trigger','procedure',
    'primary key','foreign key','schema','database','query','sql','mysql',
    'mongodb','nosql','aggregate','find','pipeline','collection','document',
    'db.','mongo','crud','migration','transaction','constraint',
    'python','django','flask','pandas','numpy','matplotlib','pip',
    'java','spring','maven','gradle','jvm','servlet','arraylist','hashmap',
    'c++','cpp','#include','printf','scanf','malloc','pointer','struct',
    'cout','cin','vector','template','namespace',
    'javascript','typescript','nodejs','react','html','css','php','ruby',
    'array','loop','for','while','function','class','object','recursion',
    'sorting','searching','fibonacci','factorial','palindrome','prime',
    'binary','stack','queue','linked list','tree','graph','algorithm',
    'data structure','string','list','pointer','inheritance','exception',
    'vowel','consonant','anagram','harshad','happy','perfect','gcd','lcm',
    'even','odd','number','series','code','program','swap','reverse',
    'pattern','star','triangle','matrix','calculator','integer','whole',
    'natural','digit','count','sum','average','max','min','sort','search',
    'insert','remove','filter','extract','reverse','check','find','print',
    'write','implement','build','make','create','read','parse','convert',
    'library','method','variable','constant','type','output','input',
    'run','execute','compile','debug','error','exception','syntax',
    'oop','interface','abstract','polymorphism','encapsulation',
    'armstrong','student','employee','table','query','number',
]

NON_PROGRAMMING_KEYWORDS = [
    'weather','cricket','movie','film','song','recipe','cook','food',
    'politics','election','sports','celebrity','news','stock','share',
    'love','relationship','joke','story','poem','essay','history',
    'geography','physics','chemistry',
]

def is_programming_topic(query):
    q = query.lower()
    if any(kw in q for kw in NON_PROGRAMMING_KEYWORDS):
        return False
    if any(kw in q for kw in DB_TOPIC_KEYWORDS):
        return True
    words = q.split()
    if len(words) <= 6:
        return True
    return False


# ── Groq API via official package (fixes Cloudflare 403) ─────────────────────
def _vision_user_content(prompt, image):
    """Build multimodal user content for Groq vision models."""
    text = (prompt or '').strip() or 'Is image ko carefully padho. Agar code, SQL, error, ya assignment dikhe to complete working solution do. Hinglish mein explain karo.'
    parts = [{'type': 'text', 'text': text}]
    if image and image.get('data'):
        mime = (image.get('mime') or 'image/jpeg').split(';')[0].strip().lower()
        if mime not in ('image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/gif'):
            mime = 'image/jpeg'
        if mime == 'image/jpg':
            mime = 'image/jpeg'
        b64 = image.get('data', '')
        if b64.startswith('data:'):
            b64 = b64.split(',', 1)[-1]
        parts.append({
            'type': 'image_url',
            'image_url': {'url': f'data:{mime};base64,{b64}'},
        })
    return parts


def call_groq(prompt, lang='', system_prompt=None, messages=None, image=None):
    """
    Call Groq using the official `groq` Python package.
    This avoids the HTTP 403 / error code 1010 Cloudflare block
    that happens with raw urllib requests.
    """
    try:
        from groq import Groq
    except ImportError:
        return None, 'groq package not installed. Run: pip install groq'

    api_key = getattr(config, 'GROQ_API_KEY', '') or os.environ.get('GROQ_API_KEY', '')
    if api_key:
        api_key = api_key.strip()
    if not api_key or 'YOUR' in api_key or not api_key.startswith('gsk_'):
        return None, 'Groq key not set or invalid (must start with gsk_)'

    preferred = getattr(config, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
    vision_preferred = getattr(config, 'GROQ_VISION_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')
    models_to_try = []
    if image:
        for candidate in (
            vision_preferred,
            'meta-llama/llama-4-scout-17b-16e-instruct',
            'meta-llama/llama-4-maverick-17b-128e-instruct',
        ):
            if candidate and candidate not in models_to_try:
                models_to_try.append(candidate)
    else:
        for candidate in (
            preferred,
            'llama-3.3-70b-versatile',
            'openai/gpt-oss-20b',
            'gemma2-9b-it',
        ):
            if candidate and candidate not in models_to_try:
                models_to_try.append(candidate)
    lang_name = lang.upper() if lang else 'Python'

    if system_prompt is None:
        system_prompt = (
            f"You are QueryNest AI — expert programmer and database engineer.\n"
            f"Active language: {lang_name}.\n"
            "RULES:\n"
            f"1. Write ONLY in {lang_name} — never switch languages\n"
            "2. Give COMPLETE, RUNNABLE code — no placeholders or '...'\n"
            "3. Add inline comment on every meaningful line\n"
            "4. Use triple backticks with language label\n"
            "5. Show expected output as a comment block at the end\n"
            "6. Answer in Hinglish (Hindi + English mix) — friendly tone\n"
            "7. NEVER output generic Hello World\n"
            "8. Explain HOW the code works in 2-3 sentences after the code"
        )

    chat_messages = [{'role': 'system', 'content': system_prompt}]

    if image:
        # Vision calls: keep short text history, attach image on the latest user turn
        if messages:
            for msg in messages[-4:]:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                if role in ('user', 'assistant') and isinstance(content, str) and content:
                    chat_messages.append({'role': role, 'content': content})
        user_content = _vision_user_content(prompt, image)
        if chat_messages and chat_messages[-1].get('role') == 'user':
            chat_messages[-1] = {'role': 'user', 'content': user_content}
        else:
            chat_messages.append({'role': 'user', 'content': user_content})
    else:
        if messages:
            for msg in messages[-6:]:
                role    = msg.get('role', 'user')
                content = msg.get('content', '')
                if role in ('user', 'assistant') and content:
                    chat_messages.append({'role': role, 'content': content})
        else:
            chat_messages.append({'role': 'user', 'content': prompt})

        if chat_messages[-1]['role'] != 'user':
            chat_messages.append({'role': 'user', 'content': prompt})

    try:
        client = Groq(api_key=api_key)
        last_err = None
        for model in models_to_try:
            try:
                completion = client.chat.completions.create(
                    model       = model,
                    messages    = chat_messages,
                    max_tokens  = 2048,
                    temperature = 0.3,
                )
                text = completion.choices[0].message.content.strip()
                if text:
                    print(f"[Groq] ✅ {model}: {len(text)} chars received")
                    return text, None
                last_err = 'Empty response from Groq'
            except Exception as e:
                last_err = str(e)
                print(f"[Groq] ❌ {model}: {last_err}")
                err_l = last_err.lower()
                if any(k in err_l for k in (
                    'model_not_found', 'does not exist', 'decommissioned',
                    'invalid model', 'unsupported', 'vision', 'image_url',
                )):
                    continue
                return None, last_err
        return None, last_err or 'No Groq model available'

    except Exception as e:
        err = str(e)
        print(f"[Groq] ❌ {err}")
        return None, err


# ── Main entry point ──────────────────────────────────────────────────────────
def call_claude_ai(prompt, lang='', system_prompt=None, messages=None, image=None):
    """Single entry point — uses Groq via official SDK (no Cloudflare block)."""
    text, err = call_groq(prompt, lang, system_prompt, messages, image=image)
    if text:
        return text, None
    return None, err


def save_ai_answer(db, query, content, language, source='ai'):
    """Cache AI answer in MongoDB."""
    if db is None:
        return
    try:
        db['solutions'].update_one(
            {'title': query},
            {'$set': {
                'title': query, 'content': content, 'language': language,
                'tags': normalize_query(query).split(), 'source': source,
            }},
            upsert=True
        )
    except Exception as e:
        print(f"Cache save error: {e}")
