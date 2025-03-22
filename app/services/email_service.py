from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import (
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM,
    MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME,
    MAIL_STARTTLS, MAIL_SSL_TLS, USE_CREDENTIALS)


# Email configuration
mail_config = ConnectionConfig()


async def send_email_response(subject, body, recipient):
    """Send email with AI-generated response"""
    # Create message
    message = MessageSchema(
        subject=f"Re: {subject}",
        recipients=[recipient],
        body=body,
        subtype="html"
    )

    # Initialize FastMail
    fm = FastMail(mail_config)

    # Send email
    await fm.send_message(message)
    return {"message": "Email sent successfully"}


