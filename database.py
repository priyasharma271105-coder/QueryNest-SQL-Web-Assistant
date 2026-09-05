"""
QueryNest — Database Connection
Single MongoDB connection shared across all modules.
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
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db               = client[DB_NAME]
        users_collection = db['users']
        try:
            db['solutions'].create_index([('title','text'),('content','text'),('tags','text')])
        except Exception:
            pass
        print(f"✅ MongoDB connected → '{DB_NAME}' | users: {users_collection.count_documents({})}")
    except Exception as e:
        print(f"⚠️  MongoDB NOT connected: {e}")
        print("   ➜  Run 'mongod' then restart app")
        db               = None
        users_collection = None

def get_db():
    return db

def get_users():
    return users_collection
