from pymongo import MongoClient


def connect_to_mongo(mongo_url):
	client = MongoClient(mongo_url)
	return client.get_default_database()
