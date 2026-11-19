"""
QueryNest — Configuration Template (config.example.py)
Copy this file to config.py and fill in your values, or provide them via .env / AWS Secrets Manager.
"""
import os
from pathlib import Path

# Load .env file automatically
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).resolve().parent / '.env'
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
except ImportError:
    pass

# Helper to fetch from Secrets Manager or environment
def _get_setting(key, default=''):
    try:
        from aws.secrets_service import get_secret_value
        val = get_secret_value(key, default)
        return val if val else default
    except Exception:
        return os.environ.get(key, default)

# ── Flask ──────────────────────────────────────────────────────
SECRET_KEY  = _get_setting('SECRET_KEY', 'querynest_secret_key_2024')
DEBUG       = os.environ.get('DEBUG', 'true').lower() == 'true'
PORT        = int(os.environ.get('PORT', 5000))

# ── MongoDB ────────────────────────────────────────────────────
MONGO_URI   = _get_setting('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME     = _get_setting('DB_NAME', 'QueryNest')

# ── Email ──────────────────────────────────────────────────────
EMAIL_ADDRESS  = _get_setting('EMAIL_ADDRESS', 'your_email@gmail.com')
EMAIL_PASSWORD = _get_setting('EMAIL_PASSWORD', 'your_app_password')
TEST_MODE      = os.environ.get('TEST_MODE', 'false').lower() == 'true'

# ── Groq AI ────────────────────────────────────────────────────
GROQ_API_KEY = _get_setting('GROQ_API_KEY', 'gsk_your_groq_api_key_here')
GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')
GROQ_VISION_MODEL = os.environ.get('GROQ_VISION_MODEL', 'meta-llama/llama-4-scout-17b-16e-instruct')

# ── Razorpay ───────────────────────────────────────────────────
RAZORPAY_KEY_ID     = _get_setting('RAZORPAY_KEY_ID',     'rzp_test_YOUR_KEY_ID')
RAZORPAY_KEY_SECRET = _get_setting('RAZORPAY_KEY_SECRET', 'YOUR_KEY_SECRET')

# ── Paths ──────────────────────────────────────────────────────
BASE_DIR            = os.path.dirname(os.path.abspath(__file__))
SAVED_QUERIES_DIR   = os.path.join(BASE_DIR, 'data', 'saved_queries')
SAVED_PROGRAMS_DIR  = os.path.join(BASE_DIR, 'data', 'saved_programs')
PDF_EXPORTS_DIR     = os.path.join(BASE_DIR, 'data', 'generated_pdfs')

# ── Premium Plans ──────────────────────────────────────────────
PREMIUM_PLANS = {
    'monthly':   {'name': 'Monthly Plan',   'price': 199,  'duration_days': 30,  'description': '1 Month Premium Access'},
    'quarterly': {'name': 'Quarterly Plan', 'price': 499,  'duration_days': 90,  'description': '3 Months Premium Access'},
    'yearly':    {'name': 'Yearly Plan',    'price': 1499, 'duration_days': 365, 'description': '1 Year Premium Access'},
}

# ── Code Execution ─────────────────────────────────────────────
EXEC_TIMEOUT = 10   # seconds per code run
