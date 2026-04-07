import os
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str, max_results: int = 3) -> list[str]:
    """
    Wrapper around Tavily search.
    Returns a clean list of result snippets.
    """
    try:
        results = tavily.search(query=query, max_results=max_results)
        return [r["content"] for r in results.get("results", [])]
    except Exception as e:
        print(f"[Search] Error: {e}")
        return ["Search failed — no results returned."]