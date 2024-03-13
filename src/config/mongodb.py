from pymongo import MongoClient
import os

coll = MongoClient(os.getenv('MONGO_URI'))['todos']['todos']
