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
    """Search local files for technical project details."""
    chunks = get_relevant_chunks(query)
    return "\n\n".join(chunks) if chunks else "No data found locally."

@tool
def web_search(query: str) -> str:
    """Search the web for real-time info and URLs."""
    try:
        # We use a broader search to capture links
        return DuckDuckGoSearchAPIWrapper().run(query)
    except:
        return "Web search unavailable."

tools = [local_document_search, web_search]
model = ChatOllama(model="llama3.1", temperature=0.1).bind_tools(tools)

# UPDATED PROMPT: Demands links and detailed output
SYSTEM_PROMPT = SystemMessage(content="""
You are a highly detailed Research Assistant. 
1. If the local search is insufficient, ALWAYS use the web search.
2. Provide long, comprehensive answers. Do not be brief.
3. If you cannot find a definitive answer, provide at least 2-3 helpful web links (URLs) related to the topic.
4. If you mention a fact from the web, try to include the source link at the end of your response.
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
