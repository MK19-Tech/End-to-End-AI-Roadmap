import os
from typing import Annotated, TypedDict, List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# Import your existing local database functions
from utils.retriever import get_relevant_chunks

# --- TOOL DEFINITIONS ---

@tool
def local_document_search(query: str) -> str:
    """Use this tool to search internal technical documents and project files for specific details stored locally."""
    try:
        # Calls your existing ChromaDB retrieval logic
        chunks = get_relevant_chunks(query)
        if isinstance(chunks, list):
            return "\n\n".join(chunks) if chunks else "No relevant documents found in local storage."
        return str(chunks)
    except Exception as e:
        return f"Error accessing local database: {e}"

@tool
def web_search(query: str) -> str:
    """Use this tool to search the internet for real-time information, news, or general knowledge not in local files."""
    try:
        search = DuckDuckGoSearchAPIWrapper()
        return search.run(query)
    except Exception as e:
        return f"Web search failed: {e}"

# --- MODEL SETUP ---

# We MUST use llama3.1:8b-instruct-q2_K because the original llama3 does not support tool calling (Error 400).
tools = [local_document_search, web_search]
model = ChatOllama(
    model="llama3.1:8b-instruct-q2_K", 
    temperature=0,
    base_url="http://localhost:11434" 
).bind_tools(tools)

# --- GRAPH LOGIC ---

def call_model(state: MessagesState):
    """The Agent node: Decides whether to use a tool or finish the conversation."""
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# Define the Graph Structure
workflow = StateGraph(MessagesState)

# Add Nodes (The 'brain' and the 'tool executor')
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Define the Edges
workflow.add_edge(START, "agent")

# Logic: Check if the model wants to use a tool (tools_condition handles this automatically)
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# After a tool is used, the result is sent back to the agent to formulate the final answer
workflow.add_edge("tools", "agent")

# Compile the final application
agent_app = workflow.compile()

# --- STANDALONE TEST LOGIC ---
if __name__ == "__main__":
    print("--- Local Agentic RAG System Testing ---")
    print("Ensure you have run: ollama pull llama3.1")
    
    test_query = "Compare my local project details with current industry web trends."
    inputs = {"messages": [HumanMessage(content=test_query)]}
    
    try:
        for output in agent_app.stream(inputs, stream_mode="values"):
            message = output["messages"][-1]
            print(f"\n[Node]: {message.type.upper()}")
            print(message.content if message.content else "{Tool Call Generated}")
    except Exception as e:
        print(f"\n[ERROR]: {e}")
