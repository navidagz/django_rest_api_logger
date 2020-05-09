from django.conf import settings

MONGO_TIMEOUT = getattr(settings, "DRF_LOGGER_MONGO_TIMEOUT_MS", 5)
MONGO_HOST = getattr(settings, "DRF_LOGGER_MONGO_HOST", None)
MONGO_LOG_DB = getattr(settings, "DRF_LOGGER_MONGO_LOG_DB", "log")
MONGO_LOG_COLLECTION = getattr(settings, "DRF_LOGGER_MONGO_LOG_COLLECTION", "logs")
log_db = None

if MONGO_HOST:
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError

    client = MongoClient(host=MONGO_HOST, serverSelectionTimeoutMS=MONGO_TIMEOUT)
    try:
        client.server_info()
        log_db = client[MONGO_LOG_DB]
    except ServerSelectionTimeoutError:
        raise Exception("Can not connect to mongo db")
