from pymongo import MongoClient

conn = MongoClient("mongodb://user:password@mongoo:27017/data?authSource=admin")
