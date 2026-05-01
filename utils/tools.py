# utils/tools.py
from utils.retriever import get_relevant_chunks
import os

def document_search(query: str):
    """Search the local vector database for technical documentation and project details."""
    chunks = get_relevant_chunks(query)
    return "\n".join(chunks)

def web_search(query: str):
    """Search the internet for real-time information or external references."""
    # Example using Tavily or DuckDuckGo (Requires: pip install duckduckgo-search)
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=3)]
        return "\n".join(results)

# Create a dictionary of available tools
TOOLS = {
    "document_search": document_search,
    "web_search": web_search
}
