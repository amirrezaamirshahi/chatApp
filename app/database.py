# app/database.py

from pymongo import MongoClient
from .config import DATABASE_URI, DATABASE_NAME

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
