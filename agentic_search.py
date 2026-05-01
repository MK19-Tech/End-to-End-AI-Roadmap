import os
from typing import Annotated, TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Import your existing local functions
from utils.retriever import get_relevant_chunks

# --- TOOL DEFINITIONS ---
def local_document_search(query: str) -> str:
    """Use this tool to search internal technical documents and project files."""
    try:
        chunks = get_relevant_chunks(query)
        return "\n\n".join(chunks) if chunks else "No relevant documents found."
    except Exception as e:
        return f"Error accessing local DB: {e}"

web_search_tool = DuckDuckGoSearchRun()

# Combine tools into a list for the LLM
tools = [local_document_search, web_search_tool]
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# --- GRAPH NODES ---
def call_model(state: MessagesState):
    """The Agent/Router node: Decides which tool to use or answers directly."""
    print("---LOG: Agent deciding next step---")
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# The ToolNode is a pre-built component that executes the chosen tools
tool_node = ToolNode(tools)

# --- GRAPH CONSTRUCTION ---
workflow = StateGraph(MessagesState)

# Define the Nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Define the Edges (Connections)
workflow.add_edge(START, "agent")

# Add a conditional path: If tool calls are present, go to 'tools', else END
workflow.add_conditional_edges(
    "agent",
    tools_condition, 
)

# After tools are run, always go back to the agent to synthesize the final answer
workflow.add_edge("tools", "agent")

# Compile the graph
agent_app = workflow.compile()

if __name__ == "__main__":
    print("--- Agentic RAG System Ready ---")
    user_input = input("How can I help you today? ")
    
    # Run the graph and stream the thought process
    inputs = {"messages": [HumanMessage(content=user_input)]}
    for output in agent_app.stream(inputs, stream_mode="values"):
        last_message = output["messages"][-1]
        
    print("\nFinal Answer:\n", last_message.content)
