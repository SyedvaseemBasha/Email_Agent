from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.7,
    max_new_tokens=512,
    top_p=0.95,
    repetition_penalty=1.15,
    huggingfacehub_api_token=os.getenv("MODEL_API_KEY")
)

# Create prompt template
email_prompt = PromptTemplate(
    input_variables=["subject", "email_body"],
    template="""
    You are an AI assistant for a company. Your task is to respond to customer emails professionally and accurately.
    
    Email Subject: {subject}
    Email Body: {email_body}
    
    Please write a helpful, friendly, and professional response to this email.
    """
)

# Create LLM chain using Runnable Sequence
email_chain = email_prompt | llm | StrOutputParser()

async def generate_response(subject: str, email_body: str) -> str:
    """Generate AI response using LangChain and Hugging Face model"""
    try:
        response = await email_chain.ainvoke({"subject": subject, "email_body": email_body})
        return response.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "We apologize, but we encountered an issue processing your request. Our team will get back to you shortly."
