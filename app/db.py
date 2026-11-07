from pymongo import DESCENDING, MonMongoClient
from app import config

_client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
_collection = _client[config.MONGO_DB]["checks"]


def init_db():
    _collection.create_index([("url", 1), ("checked_at", -1)])


def save_result(r: dict):
    _collection.insert_one(dict(r))


def get_latest():
    pipeline = [
        {"$sort": {"checked_at": -1}},
        {"$group": {"_id": "$url", "doc": {"$first": "$$ROOT"}}},
        {"$replaceRoot": {"newRoot": "$doc"}},
        {"$project": {"_id": 0}},
    ]
    return list(_collection.aggregate(pipeline))


def get_history(url: str, limit: int = 50):
    cursor = (
        (_collection.find({"url": url}, {"_id": 0}))
        .sort("checked_at", DESCENDING)
        .limit(limit)
    )
    return list(cursor)
