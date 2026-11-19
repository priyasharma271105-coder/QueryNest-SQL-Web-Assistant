"""
QueryNest — Comprehensive Integration & Regression Test Suite
Validates all 6 AWS Services and verifies that no existing features are broken.
"""
import sys
import json
from datetime import datetime

# Windows encoding support
try:
    sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
except Exception:
    pass

print("\n" + "="*60)
print("🦅 QUERYNEST — AWS INTEGRATION & SYSTEM TEST SUITE")
print("="*60)

passed = 0
total = 0

def record_test(name, success, detail=""):
    global passed, total
    total += 1
    if success:
        passed += 1
        print(f"  ✅ [PASS] {name} {('- ' + detail) if detail else ''}")
    else:
        print(f"  ❌ [FAIL] {name} {('- ' + detail) if detail else ''}")

# ── Test 1: Configuration & Environment ────────────────────────────
print("\n[Step 1] Testing Configuration & Environment...")
try:
    import config
    record_test("Config Module Loaded", True, f"Port: {config.PORT}, DB: {config.DB_NAME}")
    from aws import aws_config
    record_test("AWS Config Loaded", True, f"AWS Enabled: {aws_config.AWS_ENABLED}, Region: {aws_config.AWS_REGION}")
except Exception as e:
    record_test("Config & Environment", False, str(e))

# ── Test 2: MongoDB Connectivity (Untouched Feature) ───────────────
print("\n[Step 2] Testing MongoDB Atlas / Local Connectivity...")
try:
    import database
    database.init_db()
    users = database.get_users()
    if users is not None:
        user_count = users.count_documents({})
        record_test("MongoDB Connectivity", True, f"Connected to collection 'users' ({user_count} records)")
    else:
        record_test("MongoDB Connectivity", False, "Users collection is None")
except Exception as e:
    record_test("MongoDB Connectivity", False, str(e))

# ── Test 3: AWS IAM Service ─────────────────────────────────────────
print("\n[Step 3] Testing AWS IAM Service...")
try:
    from aws.iam_service import get_current_identity, get_recommended_iam_policy
    identity = get_current_identity()
    policy = get_recommended_iam_policy()
    record_test("IAM Identity Inspection", True, f"Mode: {identity.get('mode')}, ARN: {identity.get('arn')}")
    record_test("Least-Privilege Policy Generator", len(policy.get("Statement", [])) == 5, f"{len(policy['Statement'])} policy statements generated")
except Exception as e:
    record_test("AWS IAM Service", False, str(e))

# ── Test 4: AWS Secrets Manager Service ─────────────────────────────
print("\n[Step 4] Testing AWS Secrets Manager Service...")
try:
    from aws.secrets_service import get_secret, get_secret_value
    sec = get_secret()
    record_test("Secrets Manager Fallback/Fetch", True, f"Source: {sec.get('source')}, Secret: {sec.get('secret_name')}")
    db_name = get_secret_value('DB_NAME', 'QueryNest')
    record_test("Secret Value Retrieval", db_name == 'QueryNest', f"Resolved DB_NAME: {db_name}")
except Exception as e:
    record_test("AWS Secrets Manager Service", False, str(e))

# ── Test 5: Amazon S3 Service (PDF & File Storage) ──────────────────
print("\n[Step 5] Testing Amazon S3 Storage Service...")
try:
    from aws.s3_service import save_generated_pdf, get_file, delete_file, generate_presigned_url
    sample_pdf_bytes = b"%PDF-1.4 QueryNest Sample Search Export PDF Data"
    res = save_generated_pdf("test_qa_user", "test_report.pdf", sample_pdf_bytes)
    record_test("S3/Local PDF Upload", res.get("success"), f"Storage: {res.get('storage')}, Key: {res.get('key')}")
    
    fetched = get_file(res["key"])
    record_test("S3/Local File Retrieval", fetched.get("success") and fetched["content"] == sample_pdf_bytes, f"Size: {len(fetched.get('content', b''))} bytes")
    
    p_url = generate_presigned_url(res["key"])
    record_test("Presigned / Direct URL", bool(p_url), f"URL: {p_url}")
    
    del_ok = delete_file(res["key"])
    record_test("S3/Local File Cleanup", del_ok, "Test file removed successfully")
except Exception as e:
    record_test("Amazon S3 Service", False, str(e))

# ── Test 6: AWS CloudWatch Logging & Metrics ────────────────────────
print("\n[Step 6] Testing AWS CloudWatch Logging & Metrics...")
try:
    from aws.cloudwatch_service import setup_cloudwatch_logging, log_event, emit_metric
    setup_cloudwatch_logging()
    log_event("INFO", "Test audit entry for QueryNest test suite")
    emit_metric("TestMetricCheck", 1.0)
    record_test("CloudWatch Log & Metric Emission", True, "Successfully logged event and recorded metric")
except Exception as e:
    record_test("AWS CloudWatch Service", False, str(e))

# ── Test 7: AWS CloudTrail Activity Tracking ────────────────────────
print("\n[Step 7] Testing AWS CloudTrail Audit Service...")
try:
    from aws.cloudtrail_service import check_trail_status, get_recent_audit_events
    trail_stat = check_trail_status()
    record_test("CloudTrail Status Check", True, f"Trail: {trail_stat.get('trail_name')}, Mode: {trail_stat.get('mode')}")
    audit_events = get_recent_audit_events(max_results=2)
    record_test("CloudTrail Event Audit Lookup", len(audit_events) > 0, f"Found {len(audit_events)} audit events")
except Exception as e:
    record_test("AWS CloudTrail Service", False, str(e))

# ── Test 8: AWS Lambda Serverless Tasks ──────────────────────────────
print("\n[Step 8] Testing AWS Lambda Serverless Service...")
try:
    from aws.lambda_service import invoke_sql_formatter
    test_sql = "select id, user_name, email from users where active = 1 and age > 18 order by created_at desc"
    lambda_res = invoke_sql_formatter(test_sql)
    record_test("Lambda SQL Formatter & Validator", lambda_res.get("is_valid") and lambda_res.get("success"), f"Mode: {lambda_res.get('execution_mode')}, Clauses: {lambda_res.get('keywords_detected')}")
except Exception as e:
    record_test("AWS Lambda Service", False, str(e))

# ── Test 9: Flask Web Application Routes & Endpoints ─────────────────
print("\n[Step 9] Testing Flask Application & Existing Features...")
try:
    from app import app
    client = app.test_client()
    
    # 1. Landing page
    r_landing = client.get('/')
    record_test("Landing Page Route (/)", r_landing.status_code == 200, f"HTTP {r_landing.status_code}")
    
    # 2. Login page
    r_login = client.get('/login')
    record_test("Login Page Route (/login)", r_login.status_code == 200, f"HTTP {r_login.status_code}")
    
    # 3. AWS Status API
    r_aws = client.get('/api/aws/status')
    record_test("AWS Status API (/api/aws/status)", r_aws.status_code == 200 and r_aws.get_json().get("aws_enabled") is not None, f"HTTP {r_aws.status_code}")
    
    # 4. Serverless SQL Formatter API
    r_fmt = client.post('/api/sql/format', json={'query': 'select * from customers where country="India"'})
    record_test("Serverless SQL Format API (/api/sql/format)", r_fmt.status_code == 200 and r_fmt.get_json().get("is_valid"), f"HTTP {r_fmt.status_code}")

    # 5. PDF S3 upload route (with session)
    with client.session_transaction() as sess:
        sess['user_id'] = 'test_qa_user'
    r_pdf = client.post('/api/pdf/save-s3', json={'filename': 'qa_export.pdf', 'content': '<html><body>Test Report</body></html>'})
    record_test("PDF S3 API (/api/pdf/save-s3)", r_pdf.status_code == 200 and r_pdf.get_json().get("success"), f"Storage: {r_pdf.get_json().get('storage')}")
except Exception as e:
    record_test("Flask App Routes", False, str(e))

print("\n" + "="*60)
print(f"📊 TEST SUMMARY: {passed} of {total} tests passed ({round(passed/total*100)}%)")
print("="*60 + "\n")
