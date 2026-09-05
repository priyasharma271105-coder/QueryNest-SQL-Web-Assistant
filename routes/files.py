"""QueryNest — Saved files & programs API routes."""
import os, re, uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, session, send_file
import database as db_module
import config

files_bp = Blueprint('files', __name__)

# ── Helper functions ─────────────────────────────────────────────
def _safe(uid): return re.sub(r'[^a-zA-Z0-9_\-]','_',str(uid))

def _user_dir(uid, base):
    p = os.path.join(base, _safe(uid))
    os.makedirs(p, exist_ok=True)
    return p

def _meta_col(name):
    db = db_module.get_db()
    return db[name] if db is not None else None

LANG_EXT = {'python':'py','java':'java','c':'c','cpp':'cpp'}
LANG_CM  = {'python':'#','java':'//','c':'//','cpp':'//'}

# ══════════════════════════════════════════════════════════════════
# SAVED FILES (SQL / MongoDB queries)
# ══════════════════════════════════════════════════════════════════

def _qext(db_type): return 'js' if db_type == 'mongodb' else 'sql'

@files_bp.route('/api/saved-files/save', methods=['POST'])
def save_file():
    if 'user_id' not in session: return jsonify({'success':False,'message':'Not logged in'}), 401
    try:
        d = request.get_json()
        uid = session['user_id']
        fid = d.get('id') or ('f' + uuid.uuid4().hex[:10])
        name, db_type, desc, code = d.get('name','untitled'), d.get('db_type','sql'), d.get('description',''), d.get('code','')
        created = d.get('created_at') or datetime.now().isoformat()
        udir = _user_dir(uid, config.SAVED_QUERIES_DIR)
        fname = fid + '.' + _qext(db_type)
        fpath = os.path.join(udir, fname)
        header = f"-- File   : {name}\n-- Type   : {db_type}\n-- Saved  : {created}\n-- User   : {uid}\n"
        if desc: header += f"-- Desc   : {desc}\n"
        header += "-"*60 + "\n\n"
        with open(fpath, 'w', encoding='utf-8') as f: f.write(header + code)
        meta = {'id':fid,'user_id':uid,'name':name,'db_type':db_type,'description':desc,'filename':fname,'created_at':created}
        col = _meta_col('saved_files')
        if col is not None: col.replace_one({'id':fid,'user_id':uid}, meta, upsert=True)
        return jsonify({'success':True,'id':fid,'filename':fname})
    except Exception as e:
        return jsonify({'success':False,'message':str(e)}), 500

@files_bp.route('/api/saved-files/list', methods=['GET'])
def list_saved_files():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    col = _meta_col('saved_files')
    metas = list(col.find({'user_id':uid},{'_id':0}).sort('created_at',-1)) if col is not None else []
    udir = _user_dir(uid, config.SAVED_QUERIES_DIR)
    for m in metas:
        fp = os.path.join(udir, m.get('filename',''))
        if os.path.exists(fp):
            with open(fp,'r',encoding='utf-8') as f: lines = f.readlines()
            m['preview'] = '\n'.join(l.rstrip() for l in lines if not l.startswith('--') and l.strip())[:300]
    return jsonify({'success':True,'files':metas})

@files_bp.route('/api/saved-files/view/<fid>', methods=['GET'])
def view_saved_file(fid):
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    col = _meta_col('saved_files')
    meta = col.find_one({'id':fid,'user_id':uid},{'_id':0}) if col is not None else None
    if not meta: return jsonify({'success':False,'message':'Not found'}), 404
    fp = os.path.join(_user_dir(uid, config.SAVED_QUERIES_DIR), meta['filename'])
    if not os.path.exists(fp): return jsonify({'success':False,'message':'File missing'}), 404
    with open(fp,'r',encoding='utf-8') as f: raw = f.read()
    lines = raw.split('\n')
    start = next((i for i,l in enumerate(lines) if l.strip() and not l.startswith('--') and not l.startswith('-'*10)), 0)
    meta['code'] = '\n'.join(lines[start:]).strip()
    return jsonify({'success':True,'file':meta})

@files_bp.route('/api/saved-files/download/<fid>', methods=['GET'])
def download_saved_file(fid):
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    col = _meta_col('saved_files')
    meta = col.find_one({'id':fid,'user_id':uid}) if col is not None else None
    if not meta: return jsonify({'success':False,'message':'Not found'}), 404
    fp = os.path.join(_user_dir(uid, config.SAVED_QUERIES_DIR), meta['filename'])
    if not os.path.exists(fp): return jsonify({'success':False,'message':'Missing'}), 404
    return send_file(fp, as_attachment=True, download_name=re.sub(r'[^a-zA-Z0-9_\-\.]','_',meta['name'])+'.'+_qext(meta['db_type']))

@files_bp.route('/api/saved-files/delete', methods=['POST'])
def delete_saved_file():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    fid = request.get_json().get('id')
    col = _meta_col('saved_files')
    meta = col.find_one({'id':fid,'user_id':uid}) if col is not None else None
    if meta:
        fp = os.path.join(_user_dir(uid, config.SAVED_QUERIES_DIR), meta.get('filename',''))
        if os.path.exists(fp): os.remove(fp)
        if col is not None: col.delete_one({'id':fid,'user_id':uid})
    return jsonify({'success':True})

# ══════════════════════════════════════════════════════════════════
# SAVED PROGRAMS (Python / Java / C / C++)
# ══════════════════════════════════════════════════════════════════

@files_bp.route('/api/saved-programs/save', methods=['POST'])
def save_program():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    try:
        d = request.get_json()
        uid = session['user_id']
        pid = d.get('id') or ('p' + uuid.uuid4().hex[:10])
        name, lang, topic = d.get('name','untitled'), d.get('lang','python'), d.get('topic','')
        desc, code = d.get('description',''), d.get('code','')
        created = d.get('created_at') or datetime.now().isoformat()
        ext = LANG_EXT.get(lang,'txt'); cm = LANG_CM.get(lang,'//')
        udir = _user_dir(uid, config.SAVED_PROGRAMS_DIR)
        fname = pid + '.' + ext
        fpath = os.path.join(udir, fname)
        header = f"{cm} Program : {name}\n{cm} Language: {lang}\n{cm} Topic   : {topic}\n{cm} Saved   : {created}\n"
        if desc: header += f"{cm} Desc    : {desc}\n"
        header += (cm + ' ' + '-'*55) + '\n\n'
        with open(fpath,'w',encoding='utf-8') as f: f.write(header + code)
        meta = {'id':pid,'user_id':uid,'name':name,'lang':lang,'topic':topic,'description':desc,'filename':fname,'created_at':created}
        col = _meta_col('saved_programs')
        if col is not None: col.replace_one({'id':pid,'user_id':uid}, meta, upsert=True)
        return jsonify({'success':True,'id':pid,'filename':fname})
    except Exception as e:
        return jsonify({'success':False,'message':str(e)}), 500

@files_bp.route('/api/saved-programs/list', methods=['GET'])
def list_saved_programs():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    col = _meta_col('saved_programs')
    metas = list(col.find({'user_id':uid},{'_id':0}).sort('created_at',-1)) if col is not None else []
    udir = _user_dir(uid, config.SAVED_PROGRAMS_DIR)
    for m in metas:
        fp = os.path.join(udir, m.get('filename',''))
        cm = LANG_CM.get(m.get('lang','python'),'//')
        if os.path.exists(fp):
            with open(fp,'r',encoding='utf-8') as f: lines = f.readlines()
            m['preview'] = '\n'.join(l.rstrip() for l in lines if not l.startswith(cm) and l.strip())[:300]
    return jsonify({'success':True,'programs':metas})

@files_bp.route('/api/saved-programs/view/<pid>', methods=['GET'])
def view_saved_program(pid):
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    col = _meta_col('saved_programs')
    meta = col.find_one({'id':pid,'user_id':uid},{'_id':0}) if col is not None else None
    if not meta: return jsonify({'success':False,'message':'Not found'}), 404
    fp = os.path.join(_user_dir(uid, config.SAVED_PROGRAMS_DIR), meta['filename'])
    if not os.path.exists(fp): return jsonify({'success':False,'message':'Missing'}), 404
    with open(fp,'r',encoding='utf-8') as f: raw = f.read()
    cm = LANG_CM.get(meta.get('lang','python'),'//')
    lines = raw.split('\n')
    start = next((i for i,l in enumerate(lines) if l.strip() and not l.startswith(cm) and not l.startswith(cm[0]*10)), 0)
    meta['code'] = '\n'.join(lines[start:]).strip()
    return jsonify({'success':True,'program':meta})

@files_bp.route('/api/saved-programs/download/<pid>', methods=['GET'])
def download_saved_program(pid):
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    col = _meta_col('saved_programs')
    meta = col.find_one({'id':pid,'user_id':uid}) if col is not None else None
    if not meta: return jsonify({'success':False,'message':'Not found'}), 404
    fp = os.path.join(_user_dir(uid, config.SAVED_PROGRAMS_DIR), meta['filename'])
    if not os.path.exists(fp): return jsonify({'success':False,'message':'Missing'}), 404
    ext = LANG_EXT.get(meta['lang'],'txt')
    return send_file(fp, as_attachment=True, download_name=re.sub(r'[^a-zA-Z0-9_\-]','_',meta['name'])+'.'+ext)

@files_bp.route('/api/saved-programs/delete', methods=['POST'])
def delete_saved_program():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    uid = session['user_id']
    pid = request.get_json().get('id')
    col = _meta_col('saved_programs')
    meta = col.find_one({'id':pid,'user_id':uid}) if col is not None else None
    if meta:
        fp = os.path.join(_user_dir(uid, config.SAVED_PROGRAMS_DIR), meta.get('filename',''))
        if os.path.exists(fp): os.remove(fp)
        if col is not None: col.delete_one({'id':pid,'user_id':uid})
    return jsonify({'success':True})
