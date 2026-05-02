import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agentic_search import agent_app

# --- 1. CONFIG & AUTHENTICATION SETUP ---
# Note: Ensure st.set_page_config is the VERY FIRST streamlit command
st.set_page_config(page_title="Agentic RAG Assistant", page_icon="🤖")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- 2. LOGIN INTERFACE ---
# We call .login() without assignment to avoid the "unpacking" error
authenticator.login(location='main')

# Check status directly from session_state as per latest library updates
if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:

    # --- 3. LOGGED IN UI ---
    st.title("🤖 Local Agentic RAG")

    # --- SIDEBAR: Profile, Reset, & Export ---
    with st.sidebar:
        st.write(f"Welcome, **{st.session_state['name']}**")
        authenticator.logout('Logout', 'sidebar')
        
        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        # Export Logic
        if "messages" in st.session_state and len(st.session_state.messages) > 0:
            chat_text = "--- AGENTIC RAG SESSION EXPORT ---\n\n"
            for msg in st.session_state.messages:
                if isinstance(msg, HumanMessage):
                    chat_text += f"USER: {msg.content}\n\n"
                elif isinstance(msg, AIMessage) and msg.content:
                    chat_text += f"AI: {msg.content}\n"
                    if "source" in msg.additional_kwargs:
                        chat_text += f"SOURCE: {msg.additional_kwargs['source']}\n"
                    chat_text += "-"*30 + "\n\n"
            
            st.download_button("📄 Download Chat (.txt)", chat_text, "rag_session.txt")

    # --- 4. CHAT HISTORY MANAGEMENT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        if isinstance(message, (HumanMessage, AIMessage)) and message.content:
            role = "user" if isinstance(message, HumanMessage) else "assistant"
            with st.chat_message(role):
                st.markdown(message.content)
                if hasattr(message, "additional_kwargs") and "source" in message.additional_kwargs:
                    st.caption(f"📍 Source: {message.additional_kwargs['source']}")

    # --- 5. CHAT INPUT & AGENT EXECUTION ---
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to state and UI
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing sources..."):
                try:
                    # Run the Agentic Graph
                    inputs = {"messages": st.session_state.messages}
                    final_state = agent_app.invoke(inputs)
                    
                    # Extract used tools for Source Citations
                    sources_used = []
                    for msg in final_state["messages"]:
                        if isinstance(msg, ToolMessage):
                            sources_used.append(msg.name.replace("_", " ").title())
                    
                    unique_sources = list(set(sources_used))
                    source_text = ", ".join(unique_sources) if unique_sources else "General Knowledge"

                    # Get final text response
                    response_message = final_state["messages"][-1]
                    response_message.additional_kwargs["source"] = source_text
                    
                    # Render Final Response
                    st.markdown(response_message.content)
                    st.caption(f"📍 Source: {source_text}")
                    
                    # Save to state
                    st.session_state.messages.append(response_message)
                    
                except Exception as e:
                    st.error(f"System Error: {e}")
