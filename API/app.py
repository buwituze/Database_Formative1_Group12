from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# Connection to the database (MongoDB)
if not MONGO_URI:
    raise ValueError("MONGO_URI not set")

client = AsyncIOMotorClient(
    MONGO_URI, 
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000, 
    connectTimeoutMS=10000,
    socketTimeoutMS=10000
)

mongo_db = client[MONGO_DB]
mongo_collection = mongo_db[MONGO_COLLECTION]

app = FastAPI()

# DB schema
class SalaryRecord(BaseModel):
    Age: int
    Gender: str
    Education_Level: str
    Job_Title: str
    Years_of_Experience: int
    Salary: int

class SalaryRecordOut(SalaryRecord):
    id: str

# Helpers
def parse_mongo_item(item) -> dict:
    item["id"] = str(item["_id"])
    del item["_id"]
    return item

# Health check endpoint to test DB connection
@app.get("/health")
async def health_check():
    try:
        await client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

# Creating the CRUD routes
@app.post("/salary-records", response_model=SalaryRecordOut)
async def create_record(record: SalaryRecord, db: str = Query("mongo", enum=["mongo", "mysql"])):
    if db == "mongo":
        try:
            result = await mongo_collection.insert_one(record.dict(by_alias=True))
            return {**record.dict(), "id": str(result.inserted_id)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    raise HTTPException(status_code=501, detail="MySQL not implemented yet.")

@app.get("/salary-records/{record_id}", response_model=SalaryRecordOut)
async def read_record(record_id: str, db: str = Query("mongo", enum=["mongo", "mysql"])):
    if db == "mongo":
        try:
            record = await mongo_collection.find_one({"_id": ObjectId(record_id)})
            if record:
                return parse_mongo_item(record)
            raise HTTPException(status_code=404, detail="Record not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    raise HTTPException(status_code=501, detail="MySQL not implemented yet.")

@app.put("/salary-records/{record_id}", response_model=SalaryRecordOut)
async def update_record(record_id: str, record: SalaryRecord, db: str = Query("mongo", enum=["mongo", "mysql"])):
    if db == "mongo":
        try:
            await mongo_collection.update_one({"_id": ObjectId(record_id)}, {"$set": record.dict()})
            updated = await mongo_collection.find_one({"_id": ObjectId(record_id)})
            if updated:
                return parse_mongo_item(updated)
            raise HTTPException(status_code=404, detail="Record not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    raise HTTPException(status_code=501, detail="MySQL not implemented yet.")

@app.delete("/salary-records/{record_id}")
async def delete_record(record_id: str, db: str = Query("mongo", enum=["mongo", "mysql"])):
    if db == "mongo":
        try:
            result = await mongo_collection.delete_one({"_id": ObjectId(record_id)})
            if result.deleted_count == 1:
                return {"detail": "Record deleted"}
            raise HTTPException(status_code=404, detail="Record not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    raise HTTPException(status_code=501, detail="MySQL not implemented yet.")