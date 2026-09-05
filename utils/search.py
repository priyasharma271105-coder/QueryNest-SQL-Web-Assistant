"""QueryNest — Search: local JSON files + MongoDB solutions."""
import os, glob, re, json
from utils.helpers import normalize_query, detect_language
import config

LANG_ALIASES = {
    'sql':['sql'],'mysql':['mysql'],'mongodb':['mongodb'],
    'python':['python'],'java':['java'],'c':['c'],'cpp':['cpp','c++'],
}

def search_local_json(raw_query, forced_lang=None):
    """Search all JSON files in data/saved_queries/.

    Strict matching: generic words (create, table, select, etc.) alone
    are not enough — at least one SPECIFIC keyword from the query must
    match the result title/tags.

    Special case: if raw_query matches a language name exactly, returns
    ALL items for that language (for the saved panel listing).
    """
    GENERIC_WORDS = {
        'create','table','select','insert','update','delete','query',
        'write','make','build','find','get','print','show','run','use',
        'program','code','function','method','example','demo','basic',
        'simple','using','with','for','the','and','that','this','from',
    }

    LANG_NAMES = {'python','java','c','cpp','sql','mysql','mongodb'}

    results = []
    base = config.SAVED_QUERIES_DIR
    files = glob.glob(os.path.join(base, '**', '*.json'), recursive=True)
    q = normalize_query(raw_query).lower().strip()
    all_keywords = [w for w in re.split(r'\s+', q) if len(w) > 2]
    specific_kws = [w for w in all_keywords if w not in GENERIC_WORDS]
    allowed = set(LANG_ALIASES.get(forced_lang, [])) if forced_lang and forced_lang != 'all' else set()

    # Language-only listing mode — return all items for that language
    is_lang_only_query = q in LANG_NAMES and (not forced_lang or forced_lang == q)

    # If no specific keywords and not a lang-only query, return nothing (avoid broad dumps)
    if not specific_kws and not is_lang_only_query:
        return []

    for jfile in files:
        try:
            with open(jfile, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list): data = [data]
            for item in data:
                if not isinstance(item, dict): continue
                item_lang = (item.get('language') or item.get('db_type') or '').lower()
                if allowed and item_lang not in allowed: continue

                title_tags = (
                    (item.get('title') or '') + ' ' +
                    ' '.join(item.get('tags', []) if isinstance(item.get('tags'), list) else [])
                ).lower()
                searchable = ' '.join(str(v) for v in item.values()).lower()

                if is_lang_only_query:
                    # Return all items for the language
                    score = 10
                elif q in title_tags:
                    score = 20
                elif specific_kws and any(k in title_tags for k in specific_kws):
                    score = sum(3 for k in specific_kws if k in title_tags)
                    score += sum(1 for k in all_keywords if k in title_tags)
                elif not specific_kws and q in searchable:
                    score = 4
                else:
                    continue

                # Strict threshold: must have meaningful specific keyword match
                if score < 6:
                    continue

                content_val = item.get('content') or item.get('code') or item.get('query','')
                if content_val and not content_val.strip().startswith('```'):
                    content_str = f"**{item.get('title',raw_query)}**\n\n```{item_lang}\n{content_val.strip()}\n```"
                else:
                    content_str = content_val or ''
                results.append({
                    'source':'local_json','collection':os.path.basename(jfile),
                    'language': item_lang or 'sql',
                    'title': item.get('title', raw_query),
                    'tags': item.get('tags', []),
                    'content': content_str,
                    '_score': score
                })
        except Exception as e:
            print(f"JSON search error ({jfile}): {e}")
    results.sort(key=lambda x: x.get('_score',0), reverse=True)
    return results[:50]  # allow up to 50 for listing

def search_db(db, raw_query, forced_lang=None):
    """Search solutions collection in MongoDB."""
    if db is None: return []
    q = normalize_query(raw_query).lower()
    keywords = [w for w in re.split(r'\s+', q) if len(w) > 2]
    det_lang = forced_lang or detect_language(q)
    try:
        col = db['solutions']
        kw_or = []
        for kw in keywords:
            pat = {'$regex': kw, '$options': 'i'}
            kw_or += [{'title':pat},{'content':pat},{'tags':pat}]
        kw_or += [{'title':{'$regex':re.escape(q),'$options':'i'}}]
        filt = {'$or': kw_or} if kw_or else {}
        if det_lang: filt['language'] = det_lang
        docs = list(col.find(filt, {'_id':0}).limit(5))
        if not docs and det_lang:
            docs = list(col.find({'$or':kw_or} if kw_or else {}, {'_id':0}).limit(5))
        def score(doc):
            txt = (doc.get('title','') + ' ' + doc.get('content','')).lower()
            s = 10 if q in txt else sum(2 for k in keywords if k in txt)
            if det_lang and doc.get('language') == det_lang: s += 5
            return s
        docs.sort(key=score, reverse=True)
        for doc in docs[:3]:
            doc['source'] = 'database'
        return docs[:3]
    except Exception as e:
        print(f"DB search error: {e}")
        return []
