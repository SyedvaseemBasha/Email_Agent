
from fastapi import FastAPI, BackgroundTasks, HTTPException
from app.models.schemas import EmailQuery, EmailResponse, FeedbackModel
from app.services.llm_service import generate_response
from app.services.db_service import store_response, get_responses, store_feedback, responses_collection
from app.services.email_service import send_email_response
from app.utils.evaluator import evaluate_response_accuracy
# from app.utils.email_extractor import extract_recipient_email
from bson import ObjectId
import time
import asyncio

app = FastAPI(title="AI Email Response Agent")

@app.post("/api/email-response", response_model=EmailResponse)
async def process_email(query: EmailQuery, background_tasks: BackgroundTasks):
    start_time = time.time()
    
    try:
        # Generate AI response using LLM
        ai_response = await generate_response(query.subject, query.email_body)
        
        # Calculate response time
        response_time = round(time.time() - start_time, 2)
        
        # Evaluate response accuracy (simplified version)
        accuracy = await evaluate_response_accuracy(query.email_body, ai_response)
        
       
        
        # Store in MongoDB (asynchronously)
        response_id = await store_response(
            query.subject, 
            query.email_body, 
            ai_response, 
            response_time, 
            accuracy
        )

        # Send email in background
        background_tasks.add_task(
            send_email_response,
            query.subject,
            ai_response,
            "your_email_address"  # In production, extract from email_body/query
        )
        
        # Create response object
        response = EmailResponse(
            ai_response=ai_response,
            response_time=response_time,
            accuracy=accuracy
        )

        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/responses")
async def get_all_responses():
    """Get all stored email responses (for admin dashboard)"""
    return await get_responses()


@app.post("/api/responses/{response_id}/feedback")
async def submit_feedback(response_id: str, feedback: FeedbackModel):
    """Store user feedback on response quality"""
    try:
        feedback_id = await store_feedback(
            response_id, 
            feedback.user_rating, 
            feedback.comments
        )
        return {"message": "Feedback submitted successfully", "feedback_id": feedback_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get statistics for admin dashboard"""
    # Get total count of responses
    total_responses = await responses_collection.count_documents({})
    
    # Get average response time
    pipeline = [{"$group": {"_id": None, "avg_time": {"$avg": "$response_time"}}}]
    result = await responses_collection.aggregate(pipeline).to_list(length=1)
    avg_response_time = round(result[0]["avg_time"], 2) if result else 0
    
    # Get average accuracy
    pipeline = [{"$group": {"_id": None, "avg_accuracy": {"$avg": "$accuracy"}}}]
    result = await responses_collection.aggregate(pipeline).to_list(length=1)
    avg_accuracy = round(result[0]["avg_accuracy"], 2) if result else 0
    
    # Get distribution of accuracy ratings
    pipeline = [
        {"$group": {"_id": "$accuracy", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    accuracy_distribution = await responses_collection.aggregate(pipeline).to_list(length=5)
    
    return {
        "total_responses": total_responses,
        "avg_response_time": avg_response_time,
        "avg_accuracy": avg_accuracy,
        "accuracy_distribution": accuracy_distribution
    }
    