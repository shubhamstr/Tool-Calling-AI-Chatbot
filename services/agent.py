import os
import json

from openai import OpenAI

from tools.web_search import web_search
from tools.email_tools import prepare_email
from services.tool_definitions import tools
from services.config import OPENAI_API_KEY, OPENAI_MODEL


# --------------------------------
# Configuration
# --------------------------------

client = OpenAI(
    api_key=OPENAI_API_KEY
)

MODEL = OPENAI_MODEL

# --------------------------------
# Available Python Functions
# --------------------------------

available_functions = {
    "web_search": web_search,
    "prepare_email": prepare_email
}

# --------------------------------
# Agent Instructions
# --------------------------------

INSTRUCTIONS = """
You are a helpful AI assistant.

Available tools:

1. web_search:
   Search the internet for current information.
   Use this tool when the user asks about recent events,
   latest updates, or information requiring web research.

2. prepare_email:
   Prepare an email for user review.
   Use this tool whenever the user requests to send an email.

IMPORTANT EMAIL RULES:

- Never send emails directly.
- Always use prepare_email to prepare email details.
- Never claim an email has been sent just because it was prepared.
- The user must explicitly confirm before sending.
- Never call a sending function.
- Ask for missing recipient information instead of inventing it.

GENERAL RULES:

- Be helpful and conversational.
- Use search results when web_search is executed.
- Include relevant source URLs in web search answers.
- Do not fabricate search results.
"""

# --------------------------------
# Main Agent Function
# --------------------------------

def run_agent(messages):

    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=messages,
        tools=tools
    )

    pending_email = None

    max_tool_rounds = 5
    tool_round = 0

    # --------------------------------
    # Tool Calling Loop
    # --------------------------------

    while tool_round < max_tool_rounds:

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            break

        tool_outputs = []

        for tool_call in tool_calls:

            function_name = tool_call.name

            try:
                arguments = json.loads(tool_call.arguments)
            except json.JSONDecodeError:
                arguments = {}

            print("\n========== TOOL CALL ==========")
            print(f"Tool: {function_name}")
            print(f"Arguments: {arguments}")

            function_to_call = available_functions.get(
                function_name
            )

            if not function_to_call:

                result = {
                    "success": False,
                    "error": f"Unknown tool: {function_name}"
                }

            else:

                try:

                    result = function_to_call(**arguments)

                    # Capture email preparation result
                    if (
                        function_name == "prepare_email"
                        and result.get("status") == "awaiting_confirmation"
                    ):
                        pending_email = {
                            **result,
                            "draft_id": tool_call.call_id
                        }

                except Exception as error:

                    result = {
                        "success": False,
                        "error": str(error)
                    }

            print(f"Result: {result}")
            print("========== END TOOL CALL ==========\n")

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result)
            })

        tool_round += 1

        # Send tool results back to OpenAI
        response = client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools
        )

    # --------------------------------
    # Prevent Infinite Tool Execution
    # --------------------------------

    remaining_calls = [
        item
        for item in response.output
        if item.type == "function_call"
    ]

    if remaining_calls:
        raise RuntimeError(
            "Maximum tool execution limit reached."
        )

    # --------------------------------
    # Return Structured Response
    # --------------------------------

    return {
        "response": response.output_text,
        "pending_email": pending_email
    }