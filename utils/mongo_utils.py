import os
from pymongo import MongoClient


MONGO_URL = os.getenv('MONGO_URL', None)
assert(MONGO_URL)

MONGO_DATABASE_NAME = os.getenv('MONGO_DATABASE_NAME', None)
assert(MONGO_DATABASE_NAME)


def connect_to_mongo():
	client = MongoClient(MONGO_URL)
	return client[MONGO_DATABASE_NAME]
