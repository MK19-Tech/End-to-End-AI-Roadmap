import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from utils.retriever import get_relevant_chunks

@tool
def local_document_search(query: str) -> str:
    """Search your local PDF files for technical details."""
    try:
        chunks = get_relevant_chunks(query)
        return "\n\n".join(chunks) if chunks else "No data found in local docs."
    except Exception as e:
        return f"DB Error: {e}"

@tool
def web_search(query: str) -> str:
    """Search the web for real-time news and general info."""
    try:
        return DuckDuckGoSearchAPIWrapper().run(query)
    except Exception as e:
        return f"Web Error: {e}"

tools = [local_document_search, web_search]
model = ChatOllama(model="llama3.1", temperature=0).bind_tools(tools)

# SYSTEM PROMPT: Forces conversational output and hides JSON
SYSTEM_PROMPT = SystemMessage(content="""
You are a conversational AI. 
1. Use tools to find facts.
2. ALWAYS summarize the findings into a clear, natural response.
3. NEVER output raw JSON code or tool parameters to the user.
""")

def call_model(state: MessagesState):
    messages = [SYSTEM_PROMPT] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

agent_app = workflow.compile()
