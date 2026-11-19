"""
QueryNest — AWS Secrets Manager Service
Retrieves production secrets (MongoDB URI, API keys, JWT secrets) from AWS Secrets Manager.
Falls back safely to local environment variables (.env) in development mode.
"""
import os
import json
from aws import aws_config

def _get_secrets_client():
    session = aws_config.get_boto3_session()
    if session is None:
        return None
    try:
        return session.client('secretsmanager')
    except Exception as e:
        print(f"[Secrets Manager] Client init error: {e}")
        return None

def get_secret(secret_name: str = None) -> dict:
    """
    Fetches JSON secret key-value pairs from AWS Secrets Manager.
    If AWS is disabled or secret is not found, falls back to local environment variables.
    """
    s_name = secret_name or aws_config.AWS_SECRET_NAME
    client = _get_secrets_client()

    if client is not None:
        try:
            response = client.get_secret_value(SecretId=s_name)
            if 'SecretString' in response:
                secret_data = json.loads(response['SecretString'])
                return {
                    "source": "AWS_SECRETS_MANAGER",
                    "secret_name": s_name,
                    "secrets": secret_data
                }
        except Exception as e:
            print(f"[Secrets Manager] Could not retrieve secret '{s_name}' ({e}). Falling back to local env.")

    # Local fallback from os.environ
    local_secrets = {
        "MONGO_URI": os.environ.get("MONGO_URI", "mongodb://localhost:27017/"),
        "SECRET_KEY": os.environ.get("SECRET_KEY", "querynest_secret_key_2024"),
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
        "EMAIL_ADDRESS": os.environ.get("EMAIL_ADDRESS", "querynest2708@gmail.com"),
        "EMAIL_PASSWORD": os.environ.get("EMAIL_PASSWORD", ""),
        "RAZORPAY_KEY_ID": os.environ.get("RAZORPAY_KEY_ID", ""),
        "RAZORPAY_KEY_SECRET": os.environ.get("RAZORPAY_KEY_SECRET", "")
    }

    return {
        "source": "LOCAL_ENVIRONMENT",
        "secret_name": s_name,
        "secrets": local_secrets
    }

def get_secret_value(key: str, default: str = "") -> str:
    """
    Retrieves a single secret value by key, checking AWS Secrets Manager first, then local env.
    """
    result = get_secret()
    secrets = result.get("secrets", {})
    return secrets.get(key, os.environ.get(key, default))

def generate_secrets_payload() -> dict:
    """
    Prepares a clean JSON payload of current environment secrets
    ready to be uploaded to AWS Secrets Manager.
    """
    return {
        "MONGO_URI": os.environ.get("MONGO_URI", ""),
        "SECRET_KEY": os.environ.get("SECRET_KEY", "querynest_secret_key_2024"),
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
        "EMAIL_ADDRESS": os.environ.get("EMAIL_ADDRESS", "querynest2708@gmail.com"),
        "EMAIL_PASSWORD": os.environ.get("EMAIL_PASSWORD", ""),
        "RAZORPAY_KEY_ID": os.environ.get("RAZORPAY_KEY_ID", ""),
        "RAZORPAY_KEY_SECRET": os.environ.get("RAZORPAY_KEY_SECRET", "")
    }
