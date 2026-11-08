
tools = [
    {
        "type": "function",
        "name": "web_search",
        "description": (
            "Search the internet for current information. "
            "Use this when the user asks about recent events, "
            "latest updates, or information requiring web research."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results.",
                }
            },
            "required": ["query", "max_results"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "prepare_email",
        "description": (
            "Prepare an email for the user to review. "
            "Never send the email directly. "
            "The user must confirm before sending."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "Recipient email address"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject"
                },
                "body": {
                    "type": "string",
                    "description": "Email message body"
                }
            },
            "required": ["recipient", "subject", "body"],
            "additionalProperties": False
        },
        "strict": True
    }
]
