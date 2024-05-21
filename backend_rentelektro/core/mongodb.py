import os
from motor.motor_asyncio import AsyncIOMotorClient

# Get MongoDB connection details from environment variables
MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "rentals_db")

MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

client = AsyncIOMotorClient(MONGO_URL)

# Access the specific database
db = client[MONGO_DB_NAME]
