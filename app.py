import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# 1. Load user credentials (usually from a config.yaml)
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# 2. Create the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 3. Render the Login Widget
name, authentication_status, username = authenticator.login('main')

if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status:
    # --- YOUR EXISTING RAG CODE GOES HERE ---
    st.sidebar.write(f'Welcome *{name}*')
    authenticator.logout('Logout', 'sidebar')
    
    # [Rest of your app.py logic...]

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agentic_search import agent_app

st.set_page_config(page_title="Agentic RAG Assistant", page_icon="🤖")
st.title("🤖 Local Agentic RAG")

# --- SIDEBAR: Settings & Export ---
with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()

    st.header("Export Session")
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        # Generate export text
        chat_text = "--- AGENTIC RAG SESSION EXPORT ---\n\n"
        for msg in st.session_state.messages:
            if isinstance(msg, HumanMessage):
                chat_text += f"USER: {msg.content}\n\n"
            elif isinstance(msg, AIMessage) and msg.content:
                chat_text += f"AI: {msg.content}\n"
                if "source" in msg.additional_kwargs:
                    chat_text += f"SOURCE: {msg.additional_kwargs['source']}\n"
                chat_text += "-"*30 + "\n\n"
        
        st.download_button(
            label="📄 Download Chat (.txt)",
            data=chat_text,
            file_name="rag_session.txt",
            mime="text/plain"
        )
    else:
        st.info("No messages to export yet.")

    st.divider()
    st.info("Llama 3.1 identifies sources from Local Docs or Web Search automatically.")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT ---
for message in st.session_state.messages:
    if isinstance(message, (HumanMessage, AIMessage)) and message.content:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)
            if hasattr(message, "additional_kwargs") and "source" in message.additional_kwargs:
                st.caption(f"📍 Source: {message.additional_kwargs['source']}")

# --- USER INPUT & AGENT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing sources..."):
            try:
                inputs = {"messages": st.session_state.messages}
                final_state = agent_app.invoke(inputs)
                
                # Extract used tools for citations
                sources_used = []
                for msg in final_state["messages"]:
                    if isinstance(msg, ToolMessage):
                        sources_used.append(msg.name.replace("_", " ").title())
                
                unique_sources = list(set(sources_used))
                source_text = ", ".join(unique_sources) if unique_sources else "General Knowledge"

                response_message = final_state["messages"][-1]
                response_message.additional_kwargs["source"] = source_text
                
                st.markdown(response_message.content)
                st.caption(f"📍 Source: {source_text}")
                
                st.session_state.messages.append(response_message)
                
            except Exception as e:
                st.error(f"Error: {e}")
