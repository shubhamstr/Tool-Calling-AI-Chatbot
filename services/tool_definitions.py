
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
    }
]
