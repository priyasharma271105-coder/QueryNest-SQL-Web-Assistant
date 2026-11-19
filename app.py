"""
QueryNest — Main entry point
Modular Flask app: routes in routes/, utils in utils/, config in config.py
AWS Services Integrated: S3, IAM, CloudWatch, CloudTrail, Lambda, Secrets Manager
"""
import sys
import os

# ── Force stdout/stderr to flush immediately and support utf-8 emojis on Windows ──
try:
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
    sys.stderr.reconfigure(line_buffering=True, encoding='utf-8')
except Exception:
    pass
os.environ['PYTHONUNBUFFERED'] = '1'

from flask import Flask, jsonify, request
import config, database
import logging

# ── Create app ────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # image chat uploads

# ── Hide HTTP request logs (200, 304) but keep print() working ───
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# ── AWS CloudWatch Logging Setup ──────────────────────────────────
try:
    from aws.cloudwatch_service import setup_cloudwatch_logging
    setup_cloudwatch_logging(app)
except Exception as e:
    print(f"[AWS Warning] CloudWatch logging init failed: {e}")

# ── Init DB ───────────────────────────────────────────────────────
with app.app_context():
    database.init_db()

# ── Register blueprints ───────────────────────────────────────────
from routes.pages   import pages_bp
from routes.auth    import auth_bp
from routes.files   import files_bp
from routes.ai      import ai_bp
from routes.payment import payment_bp
from routes.profile import profile_bp

app.register_blueprint(pages_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(files_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(profile_bp)

# ── AWS Diagnostic & Serverless Endpoints ──────────────────────────
@app.route('/api/aws/status', methods=['GET'])
def aws_status():
    """
    Returns real-time health and connection status of all 6 integrated AWS services.
    """
    from aws import aws_config
    from aws.iam_service import get_current_identity
    from aws.s3_service import _get_s3_client
    from aws.cloudtrail_service import check_trail_status
    from aws.secrets_service import get_secret

    identity = get_current_identity()
    s3_connected = _get_s3_client() is not None
    trail_status = check_trail_status()
    secrets_status = get_secret()

    return jsonify({
        "aws_enabled": aws_config.AWS_ENABLED,
        "region": aws_config.AWS_REGION,
        "mode": "AWS_CLOUD" if aws_config.is_configured() else "LOCAL_DEVELOPMENT",
        "services": {
            "iam": identity,
            "s3": {
                "connected": s3_connected,
                "bucket": aws_config.S3_BUCKET_NAME,
                "storage_fallback": "Local Disk (data/)" if not s3_connected else "Amazon S3"
            },
            "cloudwatch": {
                "active": True,
                "log_group": aws_config.CLOUDWATCH_LOG_GROUP,
                "destination": "AWS CloudWatch Logs" if aws_config.is_configured() else "Local Log File (data/querynest_app.log)"
            },
            "cloudtrail": trail_status,
            "lambda": {
                "function": aws_config.LAMBDA_SQL_FORMATTER,
                "execution": "AWS Cloud Lambda" if aws_config.is_configured() else "Local Serverless Emulation"
            },
            "secrets_manager": {
                "source": secrets_status.get("source"),
                "secret_name": aws_config.AWS_SECRET_NAME
            }
        }
    })

@app.route('/api/sql/format', methods=['POST'])
def format_sql_route():
    """
    Serverless SQL query formatter and syntax validator endpoint (powered by AWS Lambda service).
    """
    from aws.lambda_service import invoke_sql_formatter
    data = request.get_json() or {}
    raw_query = data.get('query', '')
    if not raw_query:
        return jsonify({"success": False, "message": "SQL query is required"}), 400
    
    result = invoke_sql_formatter(raw_query)
    return jsonify(result)

# ── Error handlers ────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e): return jsonify({'success':False,'message':'Not found'}), 404

@app.errorhandler(500)
def server_error(e): return jsonify({'success':False,'message':'Server error'}), 500

# ── Run ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 QueryNest — Modular Edition with AWS Cloud Services")
    print("="*50)
    print(f"📡 Server running at: http://127.0.0.1:{config.PORT}")
    from aws import aws_config
    if aws_config.is_configured():
        print("☁️  AWS Cloud Mode: ACTIVE")
    else:
        print("🏠 Local Development Mode: ACTIVE (AWS services simulated locally)")
    print("="*50 + "\n")
    app.run(debug=config.DEBUG, port=config.PORT, use_reloader=False)
