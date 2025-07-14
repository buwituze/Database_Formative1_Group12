from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

async def test_mongo():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    try:
        info = await db.list_collection_names()
        print("Collections:", info)
    except Exception as e:
        print("Error:", e)

asyncio.run(test_mongo())
