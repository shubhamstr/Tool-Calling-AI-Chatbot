import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY is missing")

client = TavilyClient(api_key=api_key)

def web_search(query: str, max_results: int = 5):
    """
    Search the internet and return relevant results.

    Args:
        query: Search query.
        max_results: Maximum number of results.

    Returns:
        List of search results.
    """

    if not query.strip():
        raise ValueError("Search query cannot be empty")

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content"),
            "score": item.get("score")
        })

    return results