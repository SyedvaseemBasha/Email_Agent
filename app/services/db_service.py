import motor.motor_asyncio
from bson import ObjectId
from datetime import datetime
from app.config import MONGODB_URL, DB_NAME

# Connect to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]
responses_collection = db["email_responses"]
feedback_collection = db["user_feedback"]

async def store_response(subject, email_body, ai_response, response_time, accuracy):
    """Store email query and response in MongoDB"""
    response_doc = {
        "subject": subject,
        "email_body": email_body,
        "ai_response": ai_response,
        "response_time": response_time,
        "accuracy": accuracy,
        "timestamp": datetime.utcnow()
    }
    
    result = await responses_collection.insert_one(response_doc)
    return str(result.inserted_id)

async def get_responses():
    """Retrieve all stored responses"""
    cursor = responses_collection.find().sort("timestamp", -1)
    responses = []
    async for document in cursor:
        document["_id"] = str(document["_id"])
        responses.append(document)
    return responses

async def store_feedback(response_id, user_rating, comments=None):
    """Store user feedback on response quality"""
    feedback_doc = {
        # "response_id": ObjectId(response_id),
        "user_rating": user_rating,
        "comments": comments,
        "timestamp": datetime.utcnow()
    }
    
    result = await feedback_collection.insert_one(feedback_doc)
    
    # Update accuracy in the original response
    await responses_collection.update_one(
        {"_id": ObjectId(response_id)},
        {"$set": {"user_accuracy": user_rating}}
    )
    
    return str(result.inserted_id)

