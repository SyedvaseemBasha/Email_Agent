# AI Email Response Agent

This project is an AI-powered email response agent that automatically generates replies to incoming emails. It leverages a large language model (LLM) to understand the context of emails and craft relevant, professional responses. The system also includes features for storing responses, collecting user feedback, and providing dashboard statistics.

## Features

-   **Automated Email Response:** Uses the Mistral-7B-Instruct-v0.1 LLM to generate intelligent responses to email queries.
-   **Response Time Tracking:** Measures and records the time taken to generate each response.
-   **Accuracy Evaluation:** Employs an accuracy evaluation mechanism to assess the quality of the generated responses.
-   **User Feedback:** Allows users to provide feedback on the accuracy and quality of the responses.
-   **Data Storage:** Stores email queries, AI responses, response times, and accuracy ratings in a MongoDB database.
-   **Email Sending:** Sends the AI-generated response back to the email recipient.
-   **Admin Dashboard:** Provides statistics on total responses, average response time, average accuracy, and accuracy distribution.
-   **Asynchronous Operations:** Uses background tasks to handle database storage and email sending without blocking the main application flow.

## Technologies Used

-   **FastAPI:** For building the web API.
-   **Uvicorn:** For running the ASGI server.
-   **MongoDB:** For storing email data and feedback.
-   **Motor:** For asynchronous MongoDB operations.
-   **LangChain:** For interacting with the LLM.
-   **Hugging Face Transformers:** For the Mistral-7B-Instruct-v0.1 model.
-   **FastAPI Mail:** For sending emails.
-   **Python-dotenv:** For managing environment variables.
-   **Pydantic:** For data validation and settings management.
-   **Torch:** For tensor operations with the LLM.
-   **Accelerate:** For model acceleration.

## Project Structure
```
email-response-agent/
├── app/
│   ├── main.py             # FastAPI application entry point
│   ├── config.py           # Environment variable configuration
│   ├── models/             # Pydantic models for validation
│   │   └── schemas.py      # Data schemas (EmailQuery, FeedbackModel)
│   ├── services/           # Core services (LLM, DB, Email)
│   │   ├── llm_service.py  
│   │   ├── db_service.py   
│   │   └── email_service.py 
│   └── utils/              # Utility scripts (Evaluator, Email Extractor)
├── .env                    # Environment variables 
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation 
```

## Setup and Installation

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd Email
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**

    -   Create a `.env` file in the root directory of the project.
    -   Add the following environment variables (replace with your actual values):

    ```properties
    # MongoDB Configuration
    MONGODB_URL=mongodb://localhost:27017
    DB_NAME=email_response_agent

    # Email Configuration
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_email_password
    MAIL_FROM=your_email@gmail.com
    MAIL_PORT=587
    MAIL_SERVER=smtp.gmail.com
    MAIL_FROM_NAME=AI Email Assistant
    MAIL_STARTTLS=True
    MAIL_SSL_TLS=False
    USE_CREDENTIALS=True

    # Model Configuration
    MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
    MODEL_API_KEY=your_huggingface_api_key
    ```
    -   **Note:** For `MAIL_PASSWORD`, if you are using Gmail, you **must** create an app password. Here's how:
        1.  **Enable 2-Step Verification:** Go to your Google Account settings and enable 2-Step Verification if you haven't already.
        2.  **Go to App Passwords:** Once 2-Step Verification is enabled, go to the "App passwords" section in your Google Account security settings (you can search for "app passwords" in the Google Account search bar).
        3.  **Select App and Device:** Choose "Mail" as the app and "Other (Custom name)" as the device. Enter a name like "AI Email Agent" and click "Generate."
        4.  **Copy the App Password:** Google will generate a 16-character app password. **Copy this password** and paste it into your `.env` file as the value for `MAIL_PASSWORD`.
        5. **Important:** Store this password in a safe place. You will not be able to see it again.
    -   **Note:** For `MODEL_API_KEY`, you need to create a Hugging Face account and get an API key from your settings.

5.  **Add sender Email address**

          ```
            email-response-agent/
             ├── app/
             │   ├── main.py
           ```
     Ensure under main.py file you have to add email address of sender(whom to send) like below pic 👇.   
     ![Screenshot 2025-03-23 073835](https://github.com/user-attachments/assets/dddf000e-20a2-4f9b-8a67-c5cd67b8e17f)

6.  **Run MongoDB:**

    -   Ensure that MongoDB is running on your local machine (or update `MONGODB_URL` in `.env` if using a remote instance).

7.  **Run the Application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    -   This will start the FastAPI application. You can access the API at `http://127.0.0.1:8000`.

## API Endpoints

-   **`POST /api/email-response`**
    -   **Description:** Processes an email query and generates an AI response.
    -   **Request Body:**

        ```json
        {
            "subject": "Inquiry About Product Availability",
            "email_body": "Hello, I am interested in purchasing the XYZ Smartwatch. Can you confirm if it's available in stock and provide details on the delivery time?"
        }
        ```

    -   **Response Body:**

        ```json
        {
            "ai_response": "Hello, thank you for your interest in the XYZ Smartwatch! Yes, the product is currently in stock. Standard delivery takes 3-5 business days, while express shipping takes 1-2 business days. Let us know if you need further assistance.",
            "response_time": 1.45,
            "accuracy": 4,
            "response_id": "65xythjlxx9xx"
        }
        ```

-   **`GET /api/responses`**
    -   **Description:** Retrieves all stored email responses.
    -   **Response Body:** A list of stored responses.

-   **`POST /api/responses/{response_id}/feedback`**
    -   **Description:** Submits user feedback for a specific response.
    -   **Request Body:**
   
        ```json
        {
            "user_rating": 4,
            "comments": "The response was helpful but could have been more detailed."
        }
        ```

    -   **Response Body:**

        ```json
        {
            "message": "Feedback submitted successfully",
            "feedback_id": "65f3c1xxxxxxxxxxxx"
        }
        ```

-   **`GET /api/dashboard/stats`**
    -   **Description:** Retrieves dashboard statistics.
    -   **Response Body:**

        ```json
        {
            "total_responses": 100,
            "avg_response_time": 2.5,
            "avg_accuracy": 3.8,
            "accuracy_distribution": [
                { "_id": 1, "count": 5 },
                { "_id": 2, "count": 10 },
                { "_id": 3, "count": 30 },
                { "_id": 4, "count": 40 },
                { "_id": 5, "count": 15 }
            ]
        }
        ```

---

## 1. MongoDB Setup
### Database Connection
**File**: `app/services/db_service.py`

```python
import motor.motor_asyncio
from app.config import MONGODB_URL, DB_NAME

# Connect to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]
responses_collection = db["email_responses"]
feedback_collection = db["user_feedback"]
```

### Database Schema
#### `email_responses` Collection:
```python
response_doc = {
    "subject": subject,
    "email_body": email_body,
    "ai_response": ai_response,
    "response_time": response_time,
    "accuracy": accuracy,
    "timestamp": datetime.utcnow()
}
```
- `subject`: (string) Email subject.
- `email_body`: (string) Email content.
- `ai_response`: (string) AI-generated response.
- `response_time`: (float) Time taken to generate response.
- `accuracy`: (integer) AI response accuracy (1-5).
- `timestamp`: (datetime) Time response was generated.
- `user_accuracy`: (integer) User rating (1-5), added after feedback.

#### `user_feedback` Collection:
```python
feedback_doc = {
    "user_rating": user_rating,
    "comments": comments,
    "timestamp": datetime.utcnow()
}
```
- `user_rating`: (integer) User rating (1-5).
- `comments`: (string, optional) User feedback.
- `timestamp`: (datetime) Feedback submission time.

### Storing Data
#### Function: `store_response()`
```python
async def store_response(subject, email_body, ai_response, response_time, accuracy):
    result = await responses_collection.insert_one(response_doc)
    return str(result.inserted_id)
```
- Stores AI responses in MongoDB.
- Returns the document ID of the stored response.

#### Function: `store_feedback()`
- Stores user feedback and updates `user_accuracy` in `email_responses`.

### Retrieving Data
#### Function: `get_responses()`
```python
async def get_responses():
    cursor = responses_collection.find().sort("timestamp", -1)
    responses = []
    async for document in cursor:
        document["_id"] = str(document["_id"])
        responses.append(document)
    return responses
```
- Fetches all stored responses sorted by timestamp (newest first).

---

## 2. Email Handling
### Email Configuration
**File**: `app/services/email_service.py`
```python
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import (
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM,
    MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME,
    MAIL_STARTTLS, MAIL_SSL_TLS, USE_CREDENTIALS)

mail_config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=MAIL_STARTTLS,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    USE_CREDENTIALS=USE_CREDENTIALS,
)
```

### Sending Emails
#### Function: `send_email_response()`
```python
async def send_email_response(subject, body, recipient):
    message = MessageSchema(
        subject=f"Re: {subject}",
        recipients=[recipient],
        body=body,
        subtype="html"
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
    return {"message": "Email sent successfully"}
```
- Sends AI-generated email responses.
- Uses SMTP configuration for email dispatch.

### Triggering Email Send
**File**: `app/main.py`
#### Function: `process_email()`
```python
@app.post("/api/email-response", response_model=EmailResponse)
async def process_email(query: EmailQuery, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        send_email_response,
        query.subject,
        ai_response,
        "Syedvasimpc7@gmail.com"  # Replace with extracted email
    )
```
- Handles incoming email queries.
- Uses FastAPI BackgroundTasks to send emails asynchronously.

---

## To view a MongoDB database on your computer using its database name, follow these steps:

 - ## Using MongoDB Compass (GUI)

   1. Download & Install MongoDB Compass.

   2. Connect to MongoDB

      - Open Compass and enter your MongoDB connection string:

        ```
        mongodb://localhost:27017
        ```
      - Click "Connect".

   3. Select Your Database

      - Find your database in the left panel.

      - Click on it to explore collections and documents.

**Email Responses**
  ![Screenshot 2025-03-23 090029](https://github.com/user-attachments/assets/240732d3-01de-4ac0-ac72-e7e518199049)

**User Feedback** 
  ![Screenshot (145)](https://github.com/user-attachments/assets/70f65f9d-9237-4913-aa99-7736c186d1ab)


---------
        
## Future Improvements

-   **Advanced Accuracy Evaluation:** Implement a more sophisticated model for evaluating response accuracy.
-   **Recipient Email Extraction:** Improve the email extraction logic to handle various email formats.
-   **Model Fine-tuning:** Fine-tune the LLM on a dataset of email responses to improve performance.
-   **Error Handling:** Add more robust error handling and logging.
-   **Security:** Implement security measures for the API and data storage.
-   **UI:** Create a user interface for interacting with the system.
- **More Dashboard Stats:** Add more stats to the dashboard.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

MIT License (or specify your preferred license)
