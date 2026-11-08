import os
import resend

from services.config import RESEND_API_KEY, RESEND_FROM_EMAIL

resend.api_key = RESEND_API_KEY

FROM_EMAIL = RESEND_FROM_EMAIL

def send_email(
    recipient: str,
    subject: str,
    body: str
):
    """
    Send an email using Resend.

    This function should only be called
    after explicit user confirmation.
    """

    if not resend.api_key:
        raise ValueError("RESEND_API_KEY is missing")

    if not FROM_EMAIL:
        raise ValueError("RESEND_FROM_EMAIL is missing")

    if not recipient or not subject or not body:
        raise ValueError("Recipient, subject and body are required")

    response = resend.Emails.send({
        "from": FROM_EMAIL,
        "to": [recipient],
        "subject": subject,
        "text": body
    })

    return {
        "success": True,
        "email_id": response["id"]
    }