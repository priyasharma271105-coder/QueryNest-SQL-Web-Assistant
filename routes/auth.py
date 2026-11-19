"""QueryNest — Auth routes: register, login, OTP, forgot password, logout."""
from aws.sns_service import publish_notification
from flask import Blueprint, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import database as db_module
from utils.helpers import generate_user_id, generate_otp, send_email, is_hindi_query, translate_hindi_to_english

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/send-otp', methods=['POST'])
def send_otp():
    users = db_module.get_users()
    if users is None:
        return jsonify({'success':False,'message':'Database error'}), 500
    data = request.json
    email = data.get('email')
    if not email: return jsonify({'success':False,'message':'Email required'})
    if users.find_one({'email':email}):
        return jsonify({'success':False,'message':'Email already registered!'})
    otp = generate_otp()
    session.update({'pending_otp':otp,'otp_email':email,'otp_time':datetime.now().isoformat()})
    print(f"\n{'*'*50}", flush=True)
    print(f"🔐 OTP GENERATED for {email}: {otp}", flush=True)
    print(f"{'*'*50}\n", flush=True)
    body = f"""<div style="font-family:Arial;padding:20px;background:#667eea;border-radius:10px;">
      <div style="background:#fff;padding:30px;border-radius:10px;">
        <h2 style="color:#667eea;">🦅 QueryNest — OTP</h2>
        <p>Your OTP: <strong style="font-size:28px;color:#667eea;">{otp}</strong></p>
        <p style="color:#999;font-size:12px;">Valid for 10 minutes.</p>
      </div></div>"""
    sent = send_email(email, "QueryNest — Email Verification", body)
    if not sent: return jsonify({'success':False,'message':'Email send failed. Check connection.'})
    return jsonify({'success':True,'message':'OTP sent!'})

@auth_bp.route('/api/register', methods=['POST'])
def register():
    users = db_module.get_users()
    if users is None: return jsonify({'success':False,'message':'Database error'}), 500
    data = request.json
    name, email, phone, password, otp = (data.get(k) for k in ['name','email','phone','password','otp'])
    if 'pending_otp' not in session or session.get('otp_email') != email:
        return jsonify({'success':False,'message':'Session expired. Request OTP again.'})
    if datetime.now() - datetime.fromisoformat(session['otp_time']) > timedelta(minutes=10):
        return jsonify({'success':False,'message':'OTP expired!'})
    if session['pending_otp'] != otp:
        return jsonify({'success':False,'message':'Invalid OTP!'})
    if users.find_one({'email':email}):
        return jsonify({'success':False,'message':'Email already registered!'})
    user_id = generate_user_id()
    users.insert_one({'user_id':user_id,'name':name,'email':email,'phone':phone,
                      'password':password,'created_at':datetime.now()})
    session.update({'user_id':user_id,'name':name,'email':email})
    for k in ['pending_otp','otp_email','otp_time']: session.pop(k, None)
    print(f"✅ Registered: {user_id} ({name})")
    return jsonify({'success':True,'message':'Registration successful!','redirect':'/home'})

@auth_bp.route('/api/login', methods=['POST'])
def login():
    users = db_module.get_users()
    if users is None:
        return jsonify({
            'success': False,
            'message': 'Database error'
        }), 500

    data = request.get_json(silent=True) or {}
    email, password = data.get('email'), data.get('password')

    user = users.find_one({'email': email})
    if not user:
        return jsonify({'success': False, 'message': 'Email not registered!'})

    if user['password'] != password:
        return jsonify({'success': False, 'message': 'Invalid password!'})

    session.update({
        'user_id': user['user_id'],
        'name': user['name'],
        'email': email
    })

    print(f"✅ Login: {user['name']}")

    # AWS SNS - Successful Login Notification
    publish_notification(
        subject="QueryNest - Login Alert",
        message=(
            "A successful login was detected in QueryNest.\n"
            f"User: {user['name']}\n"
            "Event: Successful Login\n"
            "If this was not you, please secure your account."
        )
    )

    return jsonify({
        'success': True,
        'message': 'Login successful!',
        'redirect': '/home',
        'user': {
            'name': user['name'],
            'email': user['email'],
            'user_id': user['user_id']
        }
    })
    return jsonify({
        'success': True,
        'message': 'Login successful!',
        'redirect': '/home',
        'user': {
            'name': user['name'],
            'email': user['email'],
            'user_id': user['user_id']
        }
    })
@auth_bp.route('/api/forgot-password/send-otp', methods=['POST'])
def forgot_send_otp():
    users = db_module.get_users()
    data = request.json; email = data.get('email')
    if not users.find_one({'email':email}): return jsonify({'success':False,'message':'Email not registered!'})
    otp = generate_otp()
    session.update({'reset_otp':otp,'reset_email':email,'reset_otp_time':datetime.now().isoformat()})
    print(f"\n{'*'*50}", flush=True)
    print(f"🔐 RESET OTP for {email}: {otp}", flush=True)
    print(f"{'*'*50}\n", flush=True)
    send_email(email, "QueryNest — Password Reset", f"<p>Your reset OTP: <strong>{otp}</strong></p>")
    return jsonify({'success':True,'message':'Reset code sent!'})

@auth_bp.route('/api/forgot-password/reset', methods=['POST'])
def forgot_reset():
    users = db_module.get_users()
    data = request.json
    email, otp, new_pw = data.get('email'), data.get('otp'), data.get('new_password')
    if 'reset_otp' not in session or session.get('reset_email') != email:
        return jsonify({'success':False,'message':'Session expired.'})
    if session['reset_otp'] != otp: return jsonify({'success':False,'message':'Invalid OTP!'})
    users.update_one({'email':email},{'$set':{'password':new_pw}})
    for k in ['reset_otp','reset_email','reset_otp_time']: session.pop(k, None)
    return jsonify({'success':True,'message':'Password reset successful!'})

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('pages.landing'))

@auth_bp.route('/api/me')
def get_me():
    if 'user_id' not in session: return jsonify({'success':False})
    users = db_module.get_users()
    user = users.find_one({'user_id':session['user_id']}) if users is not None else None
    if user:
        return jsonify({'success':True,'user':{'name':user['name'],'email':user['email'],
                        'phone':user.get('phone',''),'user_id':user['user_id']}})
    return jsonify({'success':False,'message':'User not found'})
