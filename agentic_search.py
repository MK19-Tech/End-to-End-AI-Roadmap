import os
from typing import Annotated, TypedDict, List
# 1. Change this import
from langchain_ollama import ChatOllama 
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# Import your local functions
from utils.retriever import get_relevant_chunks

# --- TOOL DEFINITIONS ---
@tool
def local_document_search(query: str) -> str:
    """Use this tool to search internal technical documents."""
    try:
        chunks = get_relevant_chunks(query)
        return "\n\n".join(chunks) if chunks else "No relevant documents found."
    except Exception as e:
        return f"Error: {e}"

@tool
def web_search(query: str) -> str:
    """Search the internet for real-time information."""
    search = DuckDuckGoSearchAPIWrapper()
    return search.run(query)

# --- MODEL SWAP ---
# 2. Update to use Ollama (Llama 3)
# Note: Local models require a 'format="json"' or clear instructions for tool calling
tools = [local_document_search, web_search]
model = ChatOllama(model="llama3", temperature=0).bind_tools(tools)

# ... (The rest of your Graph code: call_model, workflow, etc. remains exactly the same!)
