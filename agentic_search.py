import os
from typing import Annotated, TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
# Update this import
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Import your existing local functions
from utils.retriever import get_relevant_chunks

# --- TOOL DEFINITIONS ---

@tool
def local_document_search(query: str) -> str:
    """Use this tool to search internal technical documents and project files."""
    try:
        chunks = get_relevant_chunks(query)
        # Flatten the list of strings if necessary
        if isinstance(chunks, list) and len(chunks) > 0 and isinstance(chunks[0], list):
             chunks = chunks[0]
        return "\n\n".join(chunks) if chunks else "No relevant documents found."
    except Exception as e:
        return f"Error accessing local DB: {e}"

@tool
def web_search(query: str) -> str:
    """Search the internet for real-time information, news, or external references."""
    search = DuckDuckGoSearchAPIWrapper()
    return search.run(query)

# Combine tools
tools = [local_document_search, web_search]
# Ensure you have your OPENAI_API_KEY set in your environment
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# ... (rest of the graph code remains the same)
import os
from typing import Annotated, TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
# Update this import
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Import your existing local functions
from utils.retriever import get_relevant_chunks

# --- TOOL DEFINITIONS ---

@tool
def local_document_search(query: str) -> str:
    """Use this tool to search internal technical documents and project files."""
    try:
        chunks = get_relevant_chunks(query)
        # Flatten the list of strings if necessary
        if isinstance(chunks, list) and len(chunks) > 0 and isinstance(chunks[0], list):
             chunks = chunks[0]
        return "\n\n".join(chunks) if chunks else "No relevant documents found."
    except Exception as e:
        return f"Error accessing local DB: {e}"

@tool
def web_search(query: str) -> str:
    """Search the internet for real-time information, news, or external references."""
    search = DuckDuckGoSearchAPIWrapper()
    return search.run(query)

# Combine tools
tools = [local_document_search, web_search]
# Ensure you have your OPENAI_API_KEY set in your environment
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# ... (rest of the graph code remains the same)
