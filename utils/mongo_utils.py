import os
from pymongo import MongoClient


MONGO_URL = os.getenv('MONGO_URL', None)
assert(MONGO_URL)


def connect_to_mongo():
	return MongoClient(MONGO_URL)
