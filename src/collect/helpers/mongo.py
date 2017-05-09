from pymongo import MongoClient
import os

client = MongoClient(os.environ.get('MONGODB_URI'))
db = client[os.environ.get('MONGODB_URI').split('/')[-1]]
