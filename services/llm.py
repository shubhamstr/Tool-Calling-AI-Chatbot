import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def generate_response(messages):

    response = client.responses.create(
        model=MODEL,
        input=messages
    )

    return response.output_text
