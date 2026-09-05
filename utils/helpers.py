"""QueryNest — General helpers: OTP, user ID, email, Hindi translation."""
import random, string, smtplib, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def generate_user_id():
    return 'QN' + ''.join(random.choices(string.digits, k=8))

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_email(to_email, subject, body):
    if config.TEST_MODE:
        print(f"\n{'='*50}", flush=True)
        print(f"🧪 TEST MODE — Email NOT sent (real SMTP skipped)", flush=True)
        print(f"📧 To: {to_email}", flush=True)
        print(f"📌 Subject: {subject}", flush=True)
        print(f"{'='*50}\n", flush=True)
        return True
    try:
        msg = MIMEMultipart()
        msg['From']    = config.EMAIL_ADDRESS
        msg['To']      = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        s = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        s.starttls(); s.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD.replace(' ', ''))
        s.send_message(msg); s.quit()
        print(f"✅ Email sent to {to_email}", flush=True)
        return True
    except Exception as e:
        print(f"❌ Email error: {e}", flush=True)
        return False

def send_premium_success_email(email, name, plan, expiry):
    body = f"""
<div style="font-family:'Plus Jakarta Sans',Arial,sans-serif;background:#160428;padding:30px;">
  <div style="max-width:520px;margin:0 auto;background:#1c0a30;border:1px solid rgba(139,92,246,0.3);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,#6b4ce3,#a855f7);padding:28px 30px;text-align:center;">
      <div style="font-size:42px;">🦅</div>
      <h1 style="color:#fff;margin:10px 0 4px;font-size:22px;font-weight:800;">QueryNest Premium</h1>
      <p style="color:rgba(255,255,255,0.8);margin:0;font-size:14px;">Successfully Activated!</p>
    </div>
    <div style="padding:28px 30px;">
      <p style="color:#e2d9f3;font-size:15px;margin:0 0 18px;">Hi <strong style="color:#c4b5fd;">{name}</strong>,</p>
      <p style="color:#c4b5fd;font-size:14px;line-height:1.6;margin:0 0 20px;">
        Aapka <strong>{plan['name']}</strong> successfully activate ho gaya hai! 🎉<br>
        Ab aap QueryNest ke saare premium features enjoy kar sakte hain.
      </p>
      <div style="background:rgba(107,76,227,0.15);border:1px solid rgba(107,76,227,0.3);border-radius:10px;padding:16px 18px;margin-bottom:20px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
          <span style="color:#a78bfa;font-size:13px;">Plan:</span>
          <strong style="color:#e2d9f3;font-size:13px;">{plan['name']}</strong>
        </div>
        <div style="display:flex;justify-content:space-between;">
          <span style="color:#a78bfa;font-size:13px;">Valid Till:</span>
          <strong style="color:#22c55e;font-size:13px;">{expiry.strftime('%d %B %Y')}</strong>
        </div>
      </div>
      <p style="color:#9ca3af;font-size:12px;text-align:center;margin:0;">
        🔒 QueryNest • Premium Member
      </p>
    </div>
  </div>
</div>"""
    send_email(email, "🎉 QueryNest Premium Activated!", body)


def send_premium_expiry_alert_email(email, name, plan_name, expiry, days_left):
    """Send warning email when premium is about to expire."""
    urgency_color = '#ef4444' if days_left <= 1 else '#f59e0b' if days_left <= 3 else '#6b4ce3'
    urgency_text  = 'EXPIRES TODAY!' if days_left <= 0 else f'Expires in {days_left} day{"s" if days_left != 1 else ""}!'
    body = f"""
<div style="font-family:'Plus Jakarta Sans',Arial,sans-serif;background:#160428;padding:30px;">
  <div style="max-width:520px;margin:0 auto;background:#1c0a30;border:1px solid rgba(239,68,68,0.3);border-radius:16px;overflow:hidden;">
    <div style="background:linear-gradient(135deg,{urgency_color},{urgency_color}cc);padding:24px 30px;text-align:center;">
      <div style="font-size:38px;">⏰</div>
      <h1 style="color:#fff;margin:10px 0 4px;font-size:20px;font-weight:800;">Premium Expiry Alert</h1>
      <p style="color:rgba(255,255,255,0.9);margin:0;font-size:14px;font-weight:700;">{urgency_text}</p>
    </div>
    <div style="padding:28px 30px;">
      <p style="color:#e2d9f3;font-size:15px;margin:0 0 14px;">Hi <strong style="color:#c4b5fd;">{name}</strong>,</p>
      <p style="color:#c4b5fd;font-size:14px;line-height:1.6;margin:0 0 18px;">
        Aapka <strong>{plan_name}</strong> <strong style="color:{urgency_color};">{expiry.strftime('%d %B %Y')}</strong> ko expire ho raha hai.<br>
        Premium access continue karne ke liye abhi renew karo!
      </p>
      <div style="text-align:center;margin:20px 0;">
        <a href="http://querynest.com/pricing" 
           style="display:inline-block;background:linear-gradient(135deg,#6b4ce3,#a855f7);color:#fff;padding:13px 32px;border-radius:10px;text-decoration:none;font-weight:700;font-size:15px;">
          🚀 Renew Premium Now
        </a>
      </div>
      <p style="color:#9ca3af;font-size:12px;text-align:center;margin:0;">
        QueryNest • Premium Member Reminder
      </p>
    </div>
  </div>
</div>"""
    send_email(email, f"⏰ QueryNest Premium — {urgency_text}", body)


HINDI_MAP = {
    'प्राइम नंबर': 'prime number', 'फिबोनाची': 'fibonacci', 'फैक्टोरियल': 'factorial',
    'पैलिंड्रोम': 'palindrome', 'बबल सॉर्ट': 'bubble sort', 'आर्मस्ट्रांग': 'armstrong',
    'हर्षद': 'harshad', 'स्वैप': 'swap', 'लूप': 'loop', 'ऐरे': 'array',
    'टेबल बनाओ': 'create table', 'बनाओ': 'create', 'डालो': 'insert', 'दिखाओ': 'select',
    'पायथन': 'python', 'जावा': 'java', 'का कोड दो': '', 'कोड दो': '',
    'नंबर': 'number', 'सीरीज': 'series',
    'banao': 'create', 'dikhao': 'select', 'dalo': 'insert', 'hatao': 'delete',
    'ka code do': '', 'code do': '', 'python mein': 'python', 'c mein': 'c',
    'java mein': 'java', 'sql mein': 'sql', 'mysql mein': 'mysql',
}

def is_hindi_query(text):
    return any('\u0900' <= ch <= '\u097F' for ch in text)

def translate_hindi_to_english(text):
    result = text.lower().strip()
    for h, e in HINDI_MAP.items():
        result = result.replace(h, e)
    result = re.sub(r'[\u0900-\u097F]+', ' ', result)
    return re.sub(r'\s+', ' ', result).strip()

def normalize_query(raw):
    q = raw.lower().strip()
    for h, e in HINDI_MAP.items():
        q = q.replace(h, e)
    return q.strip()

def detect_language(query):
    q = query.lower()
    if any(k in q for k in ['python', 'py ']): return 'python'
    # Java: match 'java' as whole word (handles 'fibonacci java', 'java array', etc.)
    if re.search(r'\bjava\b', q): return 'java'
    # C++ / cpp: check before bare 'c' to avoid false match
    if any(k in q for k in ['c++', 'cpp']): return 'cpp'
    # C: match word boundary or common phrases ('in c', 'c mein', etc.)
    if re.search(r'\b(in c|c mein|c language|c code)\b', q): return 'c'
    if re.search(r'\bc\b', q): return 'c'
    if any(k in q for k in ['mongodb', 'nosql', 'mongo']): return 'mongodb'
    if 'mysql' in q: return 'mysql'
    if any(k in q for k in ['sql', 'select', 'insert', 'create table', 'join']): return 'sql'
    return None
