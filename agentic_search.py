import os
from typing import Annotated, TypedDict, List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# Import your local database functions
from utils.retriever import get_relevant_chunks

# --- TOOL DEFINITIONS ---

@tool
def local_document_search(query: str) -> str:
    """Search internal technical documents and project files for specific details."""
    try:
        chunks = get_relevant_chunks(query)
        if isinstance(chunks, list):
            return "\n\n".join(chunks) if chunks else "No relevant documents found."
        return str(chunks)
    except Exception as e:
        return f"Local DB Error: {e}"

@tool
def web_search(query: str) -> str:
    """Search the internet for real-time information or general knowledge."""
    try:
        search = DuckDuckGoSearchAPIWrapper()
        return search.run(query)
    except Exception as e:
        return f"Web Search Error: {e}"

# --- MODEL SETUP ---
tools = [local_document_search, web_search]
# Using llama3.1 is required for tool support
model = ChatOllama(
    model="llama3.1", 
    temperature=0,
    base_url="http://localhost:11434"
).bind_tools(tools)

# --- GRAPH LOGIC ---

# This prompt forces the agent to use tools and then summarize the findings
SYSTEM_PROMPT = SystemMessage(content="""
You are an intelligent Assistant. 
1. Use 'local_document_search' for private files.
2. Use 'web_search' for general or real-time info.
3. After receiving tool results, write a helpful, conversational summary. 
4. DO NOT show the raw JSON tool-calls to the user.
""")

def call_model(state: MessagesState):
    """The Agent node: Routes to tools or provides a final answer."""
    messages = [SYSTEM_PROMPT] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent") # This loop ensures the agent reads the tool output

agent_app = workflow.compile()
