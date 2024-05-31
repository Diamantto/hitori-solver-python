"""Database module for MongoDB connection."""
import os
from motor.motor_asyncio import AsyncIOMotorClient

mongo_root_username = "diamantto"
mongo_root_password = "diamantto1234"
db_host = "test.snlxx5f.mongodb.net"
db_port = "27017"

# MongoDB connection URL
MONGO_URL = f"mongodb+srv://{mongo_root_username}:{mongo_root_password}@{db_host}/"
client = AsyncIOMotorClient(MONGO_URL)

DB = client[os.getenv('DB_NAME', 'main')]
