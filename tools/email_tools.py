def prepare_email(
    recipient: str,
    subject: str,
    body: str
):
    """
    Prepare an email for user review.
    Does not send the email.
    """

    if not recipient or not subject or not body:
        raise ValueError("All email fields are required")

    return {
        "status": "awaiting_confirmation",
        "recipient": recipient,
        "subject": subject,
        "body": body
    }