import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agentic_search import agent_app # Import your compiled graph

# --- PAGE CONFIG ---
st.set_page_config(page_title="Agentic RAG Assistant", page_icon="🤖")
st.title("🤖 Local Agentic RAG")
st.markdown("Query your local docs or the web using **Llama 3**.")

# --- SESSION STATE (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        st.markdown(message.content)

# --- USER INPUT ---
if prompt := st.chat_input("Ask me anything..."):
    # 1. Add user message to history and UI
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Run the Agentic Graph
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking & searching..."):
            try:
                # Prepare input for the graph
                inputs = {"messages": st.session_state.messages}
                
                # Run graph (We take the last message from the result)
                final_state = agent_app.invoke(inputs)
                response_text = final_state["messages"][-1].content
                
                # 3. Show and Save Response
                st.markdown(response_text)
                st.session_state.messages.append(AIMessage(content=response_text))
                
            except Exception as e:
                st.error(f"Error: {e}")
