import imaplib
import email
import smtplib
# import openai
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# *Config: Replace with your credentials*
EMAIL_USER = "offflow48@gmail.com"
EMAIL_PASS = "txqjfjuorqzrmged"  # Use App Password if needed
IMAP_SERVER = "imap.gmail.com"  # Change for Outlook/Yahoo
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# MAIL_USERNAME=offflow48@gmail.com
# MAIL_PASSWORD=txqjfjuorqzrmged                 #Syedvaseem7@
# MAIL_FROM=offflow48@gmail.com
# MAIL_PORT=587
# MAIL_SERVER=smtp.gmail.com
# MAIL_FROM_NAME=AI Email Assistant
# MAIL_STARTTLS=True
# MAIL_SSL_TLS=False
# USE_CREDENTIALS=True

# *Date Range for Filtering Emails*
START_DATE = "21-Mar-2025"
END_DATE = "22-Mar-2025"

# *OpenAI API Key for LLM Response Generation*
OPENAI_API_KEY = "your_openai_api_key"

# *Connect to Email Server (IMAP)*
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_USER, EMAIL_PASS)
mail.select("inbox")

# *Search for Emails within Date Range*
search_criteria = f'(SINCE {START_DATE} BEFORE {END_DATE})'
status, messages = mail.search(None, search_criteria)
email_ids = messages[0].split()



from langchain_huggingface import HuggingFaceEndpoint
import os

# ✅ Load Hugging Face API Key from environment
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# ✅ Set up the Hugging Face LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.7,
    max_new_tokens=512,
    top_p=0.95,
    repetition_penalty=1.15,
    huggingfacehub_api_token=os.getenv("MODEL_API_KEY")
)

# *Function to Generate LLM Response*
def generate_llm_response(original_email):
    """Generates an AI-powered email response using Hugging Face API."""
    prompt = f"You are an AI email responder.\n\nEmail: {original_email}\n\nProvide a professional response:"
    return llm.invoke(prompt)


# def generate_llm_response(original_email):
#     openai.api_key = OPENAI_API_KEY
#     response = openai.ChatCompletion.create(
#         model="gpt-4",  # Use GPT-4 or other LLM
#         messages=[
#             {"role": "system", "content": "You are an AI email responder."},
#             {"role": "user", "content": original_email}
#         ]
#     )
#     return response["choices"][0]["message"]["content"]

# *Function to Send Reply*
def send_reply(to_email, subject, body):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = f"Re: {subject}"
    msg.attach(MIMEText(body, "plain"))

    server.sendmail(EMAIL_USER, to_email, msg.as_string())
    server.quit()

# *Process Emails*
for email_id in email_ids:
    _, msg_data = mail.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            # Extract sender, subject, and body
            sender = email.utils.parseaddr(msg["From"])[1]
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            # *Generate LLM Response*
            llm_reply = generate_llm_response(body)

            # *Send Automatic Reply*
            send_reply(sender, subject, llm_reply)

            print(f"Replied to {sender} - {subject}")

# *Logout*
mail.logout()


# --------------------------------------------------

# import imaplib
# import email
# import smtplib
# import time
# import re
# from email.header import decode_header
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# import os
# import pytz
# from langchain_huggingface import HuggingFaceEndpoint

# # *Config: Replace with your credentials*
# EMAIL_USER = "offflow48@gmail.com"
# EMAIL_PASS = "txqjfjuorqzrmged"  # Use App Password if needed
# IMAP_SERVER = "imap.gmail.com"
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# # ✅ Set up the Hugging Face LLM
# llm = HuggingFaceEndpoint(
#     repo_id="mistralai/Mistral-7B-Instruct-v0.1",
#     temperature=0.7,
#     max_new_tokens=512,
#     top_p=0.95,
#     repetition_penalty=1.15,
#     huggingfacehub_api_token=os.getenv("MODEL_API_KEY")
# )

# # *Function to Generate LLM Response*
# def generate_llm_response(original_email):
#     """Generates an AI-powered email response using Hugging Face API."""
#     prompt = f"You are an AI email responder.\n\nEmail: {original_email}\n\nProvide a professional response:"
#     return llm.invoke(prompt)

# # *Function to Send Reply*
# def send_reply(to_email, subject, body):
#     server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#     server.starttls()
#     server.login(EMAIL_USER, EMAIL_PASS)

#     msg = MIMEMultipart()
#     msg["From"] = EMAIL_USER
#     msg["To"] = to_email
#     msg["Subject"] = f"Re: {subject}"
#     msg.attach(MIMEText(body, "plain"))

#     server.sendmail(EMAIL_USER, to_email, msg.as_string())
#     server.quit()

# # *Function to Connect to IMAP Server*
# def connect_imap():
#     mail = imaplib.IMAP4_SSL(IMAP_SERVER)
#     mail.login(EMAIL_USER, EMAIL_PASS)
#     mail.select("inbox")
#     return mail

# # *Initial IMAP Connection*
# mail = connect_imap()

# print("AI Email Responder is ACTIVE. Press Ctrl+C to stop.")

# try:
#     while True:  # ✅ Infinite loop until manually stopped
#         try:
#             status, messages = mail.search(None, "UNSEEN")  # Only fetch unread emails
#             email_ids = messages[0].split()

#             for email_id in email_ids:
#                 _, msg_data = mail.fetch(email_id, "(RFC822)")
#                 for response_part in msg_data:
#                     if isinstance(response_part, tuple):
#                         msg = email.message_from_bytes(response_part[1])

#                         sender = email.utils.parseaddr(msg["From"])[1]
#                         subject, encoding = decode_header(msg["Subject"])[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding or "utf-8")

#                         body = ""
#                         if msg.is_multipart():
#                             for part in msg.walk():
#                                 if part.get_content_type() == "text/plain":
#                                     body = part.get_payload(decode=True).decode()
#                                     break
#                         else:
#                             body = msg.get_payload(decode=True).decode()

#                         # *Generate LLM Response*
#                         llm_reply = generate_llm_response(body)

#                         # *Send Automatic Reply*
#                         send_reply(sender, subject, llm_reply)

#                         print(f"Replied to {sender} - {subject}")

#         except imaplib.IMAP4.abort:
#             print("IMAP session timed out. Reconnecting...")
#             mail = connect_imap()

#         time.sleep(30)  # ✅ Check for new emails every 30 seconds

# except KeyboardInterrupt:
#     print("\nStopping AI Email Responder...")

