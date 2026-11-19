"""
QueryNest — AWS Configuration Module
Centralizes all AWS credentials, service settings, and local development toggles.
"""
import os
from pathlib import Path

# Try to load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

# ── Master Toggle ───────────────────────────────────────────────────
# If False, QueryNest runs in 100% Offline Local Development Mode
AWS_ENABLED = os.environ.get('AWS_ENABLED', 'false').strip().lower() in ('true', '1', 'yes')

# ── AWS Core Credentials & Region ──────────────────────────────────
AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')
AWS_SNS_TOPIC_ARN = os.environ.get(
    'AWS_SNS_TOPIC_ARN', ''
).strip()
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '').strip()
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '').strip()
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN', '').strip() or None

# ── Amazon S3 Settings ──────────────────────────────────────────────
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'querynest-storage-bucket')
S3_PDF_PREFIX = 'generated_pdfs/'
S3_FILES_PREFIX = 'user_files/'

# ── AWS CloudWatch Settings ─────────────────────────────────────────
CLOUDWATCH_LOG_GROUP = os.environ.get('CLOUDWATCH_LOG_GROUP', '/querynest/app-logs')
CLOUDWATCH_LOG_STREAM = os.environ.get('CLOUDWATCH_LOG_STREAM', 'flask-server')

# ── AWS CloudTrail Settings ─────────────────────────────────────────
CLOUDTRAIL_NAME = os.environ.get('CLOUDTRAIL_NAME', 'querynest-management-trail')

# ── AWS Lambda Settings ─────────────────────────────────────────────
LAMBDA_SQL_FORMATTER = os.environ.get('LAMBDA_SQL_FORMATTER', 'querynest-sql-formatter')

# ── AWS Secrets Manager Settings ────────────────────────────────────
AWS_SECRET_NAME = os.environ.get('AWS_SECRET_NAME', 'querynest/app/secrets')

def is_configured() -> bool:
    """Returns True only if AWS is explicitly enabled and credentials are present."""
    if not AWS_ENABLED:
        return False
    return bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)

def get_boto3_session():
    """
    Returns an authenticated boto3.Session if credentials exist,
    or None if running in local development mode.
    """
    if not is_configured():
        return None
    try:
        import boto3
        kwargs = {'region_name': AWS_REGION}
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            kwargs['aws_access_key_id'] = AWS_ACCESS_KEY_ID
            kwargs['aws_secret_access_key'] = AWS_SECRET_ACCESS_KEY
            if AWS_SESSION_TOKEN:
                kwargs['aws_session_token'] = AWS_SESSION_TOKEN
        return boto3.Session(**kwargs)
    except Exception as e:
        print(f"[AWS Config] Error initializing boto3 session: {e}")
        return None
