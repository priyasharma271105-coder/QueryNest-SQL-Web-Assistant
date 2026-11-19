"""
QueryNest — Database Connection
Single MongoDB connection shared across all modules.
Supports MongoDB Atlas URI with seamless fallback to local MongoDB instance.
"""
try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    print("⚠️  pymongo not installed. Run: pip install pymongo")

from config import MONGO_URI, DB_NAME

client = None
db     = None
users_collection = None

def init_db():
    global client, db, users_collection
    if not PYMONGO_AVAILABLE:
        print("⚠️  MongoDB skipped — pymongo not installed")
        return
    print("🔌 Connecting to MongoDB...")

    # Determine URIs to attempt: primary config URI, then local instance fallback
    uris_to_try = []
    if MONGO_URI and "<db_password>" not in MONGO_URI and "<password>" not in MONGO_URI:
        uris_to_try.append(MONGO_URI)
    if "mongodb://localhost:27017/" not in uris_to_try:
        uris_to_try.append("mongodb://localhost:27017/")

    connected = False
    for uri in uris_to_try:
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            db               = client[DB_NAME]
            users_collection = db['users']
            try:
                db['solutions'].create_index([('title','text'),('content','text'),('tags','text')])
            except Exception:
                pass
            print(f"✅ MongoDB connected → '{DB_NAME}' | users: {users_collection.count_documents({})}")
            connected = True
            break
        except Exception:
            continue

    if not connected:
        print(f"⚠️  MongoDB NOT connected.")
        print("   ➜  Check your MongoDB Atlas connection string or ensure local 'mongod' is running.")
        db               = None
        users_collection = None

def get_db():
    return db

def get_users():
    return users_collection
