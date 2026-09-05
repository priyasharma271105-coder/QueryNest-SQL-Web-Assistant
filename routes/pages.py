"""QueryNest — Page routes (HTML rendering)."""
from flask import Blueprint, render_template, session, redirect, url_for
import database as db_module
import config

pages_bp = Blueprint('pages', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('pages.login_page'))
        return f(*args, **kwargs)
    return wrapper

@pages_bp.route('/')
def landing(): return render_template('landing.html')

@pages_bp.route('/login')
def login_page(): return render_template('login.html')

@pages_bp.route('/register')
def register_page(): return render_template('register.html')

@pages_bp.route('/forgot-password')
def forgot_password_page(): return render_template('forgot_password.html')

@pages_bp.route('/dashboard')
@login_required
def dashboard_page(): return render_template('dashboard.html')

@pages_bp.route('/search-choose')
@login_required
def search_choose_page(): return render_template('search_choose.html')

@pages_bp.route('/home')
@login_required
def home():
    users = db_module.get_users()
    user = users.find_one({'user_id':session['user_id']}) if users is not None else None
    return render_template('home.html', user=user)

@pages_bp.route('/home-premium')
@login_required
def home_premium(): return render_template('home_premium.html')

@pages_bp.route('/ide')
@login_required
def ide_page(): return render_template('ide.html')

@pages_bp.route('/pricing')
@login_required
def pricing_page(): return render_template('pricing.html', plans=config.PREMIUM_PLANS)

@pages_bp.route('/queries')
@login_required
def queries_page(): return render_template('queries.html')

@pages_bp.route('/saved-files')
@login_required
def saved_files_page(): return render_template('saved_files.html')

@pages_bp.route('/saved-programs')
@login_required
def saved_programs_page(): return render_template('saved_programs.html')

@pages_bp.route('/admin')
@login_required
def admin_page():
    db = db_module.get_db()
    users = db_module.get_users()
    stats = {}
    all_users = []
    saved_files = []
    saved_programs = []
    if db is not None and users is not None:
        all_users = list(users.find({}, {'_id':0,'password':0}).sort('created_at',-1))
        saved_files = list(db['saved_files'].find({}, {'_id':0}).sort('created_at',-1))
        saved_programs = list(db['saved_programs'].find({}, {'_id':0}).sort('created_at',-1))
        stats = {
            'total_users': users.count_documents({}),
            'total_files': db['saved_files'].count_documents({}),
            'total_programs': db['saved_programs'].count_documents({}),
        }
    # Convert datetime to string for template
    import json
    from datetime import datetime
    def dt_fix(items):
        for item in items:
            for k,v in item.items():
                if isinstance(v, datetime):
                    item[k] = v.strftime('%d %b %Y, %H:%M')
        return items
    return render_template('admin.html',
        stats=stats,
        all_users=dt_fix(all_users),
        saved_files=dt_fix(saved_files),
        saved_programs=dt_fix(saved_programs)
    )
