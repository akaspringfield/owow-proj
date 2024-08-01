from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["filedatabase"]

# Declaring the collection
users_collection = db["users"] # For user data storage
files_collection = db["files"] # For file data storage

