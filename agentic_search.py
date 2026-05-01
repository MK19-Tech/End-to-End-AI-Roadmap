import os
from typing import Annotated, TypedDict, List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# Import your existing local functions
from utils.retriever import get_relevant_chunks

# --- TOOL DEFINITIONS ---

@tool
def local_document_search(query: str) -> str:
    """Use this tool to search internal technical documents and project files for specific details."""
    try:
        # This calls your existing ChromaDB logic
        chunks = get_relevant_chunks(query)
        if isinstance(chunks, list):
            return "\n\n".join(chunks) if chunks else "No relevant documents found."
        return str(chunks)
    except Exception as e:
        return f"Error accessing local database: {e}"

@tool
def web_search(query: str) -> str:
    """Use this tool to search the internet for real-time information, news, or general knowledge."""
    try:
        search = DuckDuckGoSearchAPIWrapper()
        return search.run(query)
    except Exception as e:
        return f"Web search failed: {e}"

# --- MODEL SETUP ---

# We use Llama 3 via Ollama. Ensure 'ollama run llama3' has been executed once.
tools = [local_document_search, web_search]
model = ChatOllama(
    model="llama3", 
    temperature=0,
    base_url="http://localhost:11434" # Standard Ollama port
).bind_tools(tools)

# --- GRAPH LOGIC ---

def call_model(state: MessagesState):
    """The decision-making node: Routes to tools or provides a final answer."""
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# Define the Graph
workflow = StateGraph(MessagesState)

# Add Nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Define Flow
workflow.add_edge(START, "agent")

# Logic: If the model generated a 'tool_call', go to tools. Otherwise, END.
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# After using a tool, go back to the agent to summarize the result
workflow.add_edge("tools", "agent")

# Compile the final application
agent_app = workflow.compile()

# --- STANDALONE TEST ---
if __name__ == "__main__":
    print("--- Local Agentic RAG System Testing ---")
    print("(Ensure Ollama is running and Llama 3 is pulled)")
    
    test_query = "Search my documents for project details"
    inputs = {"messages": [HumanMessage(content=test_query)]}
    
    try:
        for output in agent_app.stream(inputs, stream_mode="values"):
            message = output["messages"][-1]
            print(f"\n[Node]: {message.type.upper()}")
            print(message.content)
    except Exception as e:
        print(f"\n[ERROR]: {e}")
        print("Check if Ollama is running (llama icon in system tray).")
