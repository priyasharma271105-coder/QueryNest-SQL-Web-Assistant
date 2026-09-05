"""QueryNest — Profile routes: stats, history, admin."""
from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
import database as db_module

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile/stats', methods=['GET'])
def get_profile_stats():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    try:
        uid   = session['user_id']
        users = db_module.get_users()
        db    = db_module.get_db()
        user  = (users.find_one({'user_id':uid},{'_id':0}) if users is not None else None) or {}

        total_searches = user.get('total_searches', 0)
        saved_files = saved_programs = 0
        if db is not None:
            try: saved_files    = db['saved_files'].count_documents({'user_id':uid})
            except: pass
            try: saved_programs = db['saved_programs'].count_documents({'user_id':uid})
            except: pass

        # Day streak
        streak = 0
        from datetime import date
        dates = set()
        for h in user.get('search_history', []):
            try: dates.add(h.get('searched_at','')[:10])
            except: pass
        today = date.today()
        for i in range(30):
            if (today - timedelta(days=i)).isoformat() in dates: streak += 1
            else: break

        is_premium = user.get('premium', False)
        expiry     = user.get('premium_expiry')
        if is_premium and expiry and expiry < datetime.now(): is_premium = False
        history = list(reversed(user.get('search_history', [])[-20:]))

        return jsonify({
            'success':True,
            'total_searches': total_searches,
            'saved_files':    saved_files,
            'saved_programs': saved_programs,
            'total_saved':    saved_files + saved_programs,
            'streak':         streak,
            'is_premium':     is_premium,
            'premium_plan':   user.get('premium_plan',''),
            'premium_expiry': expiry.strftime('%d %B %Y') if expiry and is_premium else '',
            'days_left':      (expiry-datetime.now()).days if expiry and is_premium else 0,
            'history':        history,
            'name':           user.get('name',''),
            'email':          user.get('email',''),
            'phone':          user.get('phone',''),
        })
    except Exception as e:
        return jsonify({'success':False,'message':str(e)}), 500

@profile_bp.route('/api/profile/history', methods=['GET'])
def get_history():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    users = db_module.get_users()
    if users is None: return jsonify({'success':True,'history':[],'total_searches':0})
    user = users.find_one({'user_id':session['user_id']},{'_id':0}) or {}
    history = list(reversed(user.get('search_history',[])[-50:]))
    return jsonify({'success':True,'history':history,'total_searches':user.get('total_searches',0)})

@profile_bp.route('/api/profile/history/clear', methods=['POST'])
def clear_history():
    if 'user_id' not in session: return jsonify({'success':False}), 401
    users = db_module.get_users()
    if users is not None:
        users.update_one({'user_id':session['user_id']},{'$set':{'search_history':[],'total_searches':0}})
    return jsonify({'success':True,'message':'History cleared'})

@profile_bp.route('/api/admin/clear-cache', methods=['GET'])
def clear_cache():
    if request.args.get('secret') != 'qnadmin2024': return jsonify({'error':'Unauthorized'}), 403
    db = db_module.get_db()
    if db is None: return jsonify({'error':'No DB'}), 500
    result = db['solutions'].delete_many({'source':{'$in':['gemini_chat','claude_ai','smart_gen','builtin']}})
    return jsonify({'success':True,'deleted':result.deleted_count})

@profile_bp.route('/api/admin/activate', methods=['GET'])
def admin_activate():
    import config
    if request.args.get('secret') != 'qnadmin2024': return jsonify({'error':'Unauthorized'}), 403
    order_id = request.args.get('order','').strip()
    db = db_module.get_db(); users = db_module.get_users()
    if db is None: return jsonify({'error':'No DB'}), 500
    order = db['orders'].find_one({'order_id':order_id})
    if not order: return jsonify({'error':'Order not found'}), 404
    plan_key = order.get('plan')
    uid      = order.get('user_id')
    plan     = config.PREMIUM_PLANS.get(plan_key)
    if not plan: return jsonify({'error':'Invalid plan'}), 400
    now    = datetime.now()
    expiry = now + timedelta(days=plan['duration_days'])
    users.update_one({'user_id':uid},{'$set':{'premium':True,'premium_plan':plan_key,
        'premium_activated_at':now,'premium_expiry':expiry,'expiry_alert_sent':False}})
    db['orders'].update_one({'order_id':order_id},{'$set':{'status':'completed','activated_at':now}})
    return jsonify({'success':True,'message':f'Premium activated for {uid}','expiry':expiry.strftime('%d %B %Y')})

@profile_bp.route('/debug-session')
def debug_session():
    return jsonify({'session':dict(session)})
