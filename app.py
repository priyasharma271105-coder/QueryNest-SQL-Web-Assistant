"""
QueryNest — Main entry point
Modular Flask app: routes in routes/, utils in utils/, config in config.py
"""
import sys
import os

# ── Force stdout/stderr to flush immediately (fixes missing prints) ──
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)
os.environ['PYTHONUNBUFFERED'] = '1'

from flask import Flask
import config, database
import logging

# ── Create app ────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# ── Hide HTTP request logs (200, 304) but keep print() working ───
logging.getLogger('werkzeug').setLevel(logging.ERROR)

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

# ── Error handlers ────────────────────────────────────────────────
from flask import jsonify

@app.errorhandler(404)
def not_found(e): return jsonify({'success':False,'message':'Not found'}), 404

@app.errorhandler(500)
def server_error(e): return jsonify({'success':False,'message':'Server error'}), 500

# ── Run ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 QueryNest — Modular Edition")
    print("="*50)
    print(f"📡 http://127.0.0.1:{config.PORT}")
    
    print("="*50 + "\n")
    app.run(debug=config.DEBUG, port=config.PORT, use_reloader=False)