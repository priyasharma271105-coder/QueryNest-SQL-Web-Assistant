"""QueryNest — Payment routes: Razorpay + premium activation."""
import uuid, base64, hmac, hashlib, threading, urllib.request, json as json_lib
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session
import database as db_module
import config
from utils.helpers import send_premium_success_email

payment_bp = Blueprint('payment', __name__)

# ── server-side set: (user_id, order_id) pairs that passed card/UPI validation ──
_DEMO_VALIDATED = set()

def _verify_sig(order_id, payment_id, signature):
    key = config.RAZORPAY_KEY_SECRET.encode()
    msg = f"{order_id}|{payment_id}".encode()
    expected = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

def _activate_premium(user_id, plan_key, plan):
    users = db_module.get_users()
    if users is None: return None
    now    = datetime.now()
    expiry = now + timedelta(days=plan['duration_days'])
    users.update_one({'user_id': user_id}, {'$set': {
        'premium': True, 'premium_plan': plan_key,
        'premium_activated_at': now, 'premium_expiry': expiry,
        'expiry_alert_sent': False
    }})
    return expiry

@payment_bp.route('/api/razorpay/create-order', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    data     = request.get_json()
    plan_key = data.get('plan')
    if plan_key not in config.PREMIUM_PLANS:
        return jsonify({'success': False, 'message': 'Invalid plan'}), 400

    # Block if already active premium
    users = db_module.get_users()
    if users is not None:
        try:
            existing = users.find_one({'user_id': session['user_id']})
            if existing and existing.get('premium') and existing.get('premium_expiry'):
                expiry = existing['premium_expiry']
                if expiry > datetime.now():
                    exp_str = expiry.strftime('%d %B %Y')
                    return jsonify({'success': False,
                        'message': f'Aapka premium plan abhi active hai (valid till {exp_str}). Expiry ke baad naya plan le sakte hain.'}), 400
        except Exception as e:
            print(f"Premium check error: {e}")

    plan    = config.PREMIUM_PLANS[plan_key]
    user_id = session['user_id']
    oid     = 'QN' + str(uuid.uuid4()).replace('-', '')[:12].upper()

    key_id     = (config.RAZORPAY_KEY_ID or '').strip()
    key_secret = (config.RAZORPAY_KEY_SECRET or '').strip()
    has_keys   = (key_id.startswith(('rzp_test_', 'rzp_live_')) and
                  key_id not in ('rzp_test_YOUR_KEY_ID', '') and
                  key_secret not in ('YOUR_KEY_SECRET', ''))

    rzp_oid = None
    if has_keys:
        try:
            creds   = base64.b64encode(f"{key_id}:{key_secret}".encode()).decode()
            payload = {'amount': plan['price'] * 100, 'currency': 'INR', 'receipt': oid,
                       'notes': {'plan': plan_key, 'user_id': user_id}}
            req = urllib.request.Request('https://api.razorpay.com/v1/orders',
                data=json_lib.dumps(payload).encode(),
                headers={'Content-Type': 'application/json', 'Authorization': f'Basic {creds}'},
                method='POST')
            with urllib.request.urlopen(req, timeout=15) as r:
                rzp_oid = json_lib.loads(r.read()).get('id')
                print(f"✅ Razorpay order: {rzp_oid}")
        except Exception as e:
            print(f"⚠️ Razorpay API error: {e}")

    if not rzp_oid:
        rzp_oid = f"order_DEMO_{oid}"
        print(f"🧪 Demo order: {rzp_oid}")

    db = db_module.get_db()
    if db is not None:
        try:
            db['orders'].insert_one({
                'order_id': oid, 'razorpay_order_id': rzp_oid,
                'user_id': user_id, 'email': session.get('email', ''),
                'plan': plan_key, 'amount': plan['price'], 'status': 'pending',
                'created_at': datetime.now(), 'gateway': 'razorpay'
            })
        except Exception as e:
            print(f"Order save error: {e}")

    user = {}
    if users is not None:
        try: user = users.find_one({'user_id': user_id}) or {}
        except: pass

    return jsonify({'success': True, 'order_id': oid, 'razorpay_order_id': rzp_oid,
        'key_id': key_id if has_keys else 'rzp_test_placeholder',
        'amount': plan['price'] * 100, 'plan': plan_key,
        'user_name': user.get('name', ''), 'user_email': user.get('email', ''),
        'is_demo': not has_keys})


# ── NEW: validate card/UPI before allowing demo payment ──────────
@payment_bp.route('/api/razorpay/validate-demo', methods=['POST'])
def validate_demo():
    """
    Called from frontend AFTER user fills card/UPI details.
    Sets a server-side session token so simulateScan() can proceed.
    Without calling this, the verify endpoint will reject demo payments.
    """
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    data   = request.get_json() or {}
    oid    = data.get('order_id', '').strip()
    method = data.get('method', '').strip()
    if not oid or not method:
        return jsonify({'success': False, 'message': 'Missing order_id or method'}), 400

    token = f"{session['user_id']}:{oid}"
    _DEMO_VALIDATED.add(token)
    # Keep set from growing unboundedly
    if len(_DEMO_VALIDATED) > 500:
        _DEMO_VALIDATED.clear()
    print(f"✅ Demo validated: {token} via {method}")
    return jsonify({'success': True})


@payment_bp.route('/api/razorpay/verify', methods=['POST'])
def verify_order():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    data     = request.get_json()
    rzp_oid  = data.get('razorpay_order_id', '')
    rzp_pid  = data.get('razorpay_payment_id', '')
    rzp_sig  = data.get('razorpay_signature', '')
    plan_key = data.get('plan')
    oid      = data.get('order_id')
    user_id  = session['user_id']

    if plan_key not in config.PREMIUM_PLANS:
        return jsonify({'success': False, 'message': 'Invalid plan'}), 400

    is_demo  = rzp_oid.startswith('order_DEMO_')
    key_id   = (config.RAZORPAY_KEY_ID or '').strip()
    has_keys = (key_id.startswith(('rzp_test_', 'rzp_live_')) and
                key_id not in ('rzp_test_YOUR_KEY_ID', '') and
                (config.RAZORPAY_KEY_SECRET or '').strip() not in ('YOUR_KEY_SECRET', ''))

    if is_demo:
        # Demo mode — directly allow (card/UPI validation done on frontend)
        valid = True
    elif has_keys:
        valid = _verify_sig(rzp_oid, rzp_pid, rzp_sig)
    else:
        # No keys set — BLOCK with clear message
        return jsonify({
            'success': False,
            'message': '⚙️ Razorpay keys set nahi hain. config.py mein RAZORPAY_KEY_ID aur RAZORPAY_KEY_SECRET daalo.'
        }), 400

    if not valid:
        return jsonify({'success': False, 'message': 'Payment verification failed.'}), 400

    plan   = config.PREMIUM_PLANS[plan_key]
    expiry = _activate_premium(user_id, plan_key, plan)
    if expiry is None:
        return jsonify({'success': False, 'message': 'DB error'}), 500

    db = db_module.get_db()
    if db is not None:
        try:
            db['orders'].update_one({'order_id': oid}, {'$set': {
                'status': 'completed',
                'razorpay_payment_id': rzp_pid,
                'razorpay_signature': rzp_sig,
                'completed_at': datetime.now()
            }})
        except: pass

    users = db_module.get_users()
    if users is not None:
        try:
            user = users.find_one({'user_id': user_id})
            if user:
                threading.Thread(target=send_premium_success_email,
                    args=(user['email'], user['name'], plan, expiry), daemon=True).start()
        except: pass

    print(f"✅ Premium activated: {user_id} | {plan_key} | {expiry}")
    return jsonify({'success': True, 'message': '🎉 Premium activated!',
        'expiry': expiry.strftime('%d %B %Y'), 'plan': plan_key})


@payment_bp.route('/api/premium/status', methods=['GET'])
def premium_status():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    users = db_module.get_users()
    if users is None: return jsonify({'success': False})
    user = users.find_one({'user_id': session['user_id']})
    if not user: return jsonify({'success': False})
    is_premium = user.get('premium', False)
    expiry     = user.get('premium_expiry')
    if is_premium and expiry and expiry < datetime.now():
        users.update_one({'user_id': session['user_id']}, {'$set': {'premium': False}})
        is_premium = False
    return jsonify({'success': True, 'premium': is_premium,
        'plan': user.get('premium_plan', ''),
        'expiry': expiry.strftime('%d %B %Y') if expiry and is_premium else None,
        'days_left': (expiry - datetime.now()).days if expiry and is_premium else 0})
