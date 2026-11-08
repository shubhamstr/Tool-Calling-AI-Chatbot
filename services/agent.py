import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from tools.web_search import web_search
from services.tool_definitions import tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Map available tools to Python functions
available_functions = {
    "web_search": web_search
}

def run_agent(user_message):

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are a helpful AI assistant. "
            "Use web_search when current information is needed. "
            "When using web search, provide relevant source URLs."
        ),
        input=user_message,
        tools=tools
    )

    # Process tool calls
    while True:

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            break

        tool_outputs = []

        for tool_call in tool_calls:

            function_name = tool_call.name
            arguments = json.loads(tool_call.arguments)

            function_to_call = available_functions.get(function_name)

            if not function_to_call:
                result = {"error": "Unknown tool"}
            else:
                try:
                    result = function_to_call(**arguments)
                except Exception as error:
                    result = {"error": str(error)}

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result)
            })

        response = client.responses.create(
            model=MODEL,
            instructions=(
                "Answer the user using the tool results. "
                "Include relevant source URLs."
            ),
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools
        )

    return response.output_text