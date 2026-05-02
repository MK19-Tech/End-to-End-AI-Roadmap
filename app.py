import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agentic_search import agent_app

# --- 1. AUTHENTICATION & CONFIG ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

st.set_page_config(page_title="Agentic RAG Assistant", page_icon="🤖")

# Create a list of allowed emails from config
allowed_emails = [user['email'] for user in config['credentials']['usernames'].values()]

# --- 2. CUSTOM PASSWORDLESS LOGIN ---
st.title("🤖 Local Agentic RAG")

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

# Custom Login Form
if not st.session_state["authentication_status"]:
    with st.form("login_form"):
        email_input = st.text_input("Enter your Email to Login")
        submit = st.form_submit_button("Login")
        
        if submit:
            if email_input in allowed_emails:
                # Find the user's name
                user_data = next(item for item in config['credentials']['usernames'].values() if item["email"] == email_input)
                st.session_state["authentication_status"] = True
                st.session_state["name"] = user_data["name"]
                st.rerun()
            else:
                st.error("Email not found in access list.")

# --- 3. PROTECTED CONTENT ---
if st.session_state["authentication_status"]:
    
    with st.sidebar:
        st.write(f"Welcome, **{st.session_state['name']}**")
        if st.button("Logout"):
            st.session_state["authentication_status"] = None
            st.rerun()
        
        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # --- CHAT DISPLAY ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        # HIDE JSON: Only show Human or AI messages with content
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage) and message.content.strip():
            with st.chat_message("assistant"):
                st.markdown(message.content)
                if "source" in message.additional_kwargs:
                    st.caption(f"📍 Source: {message.additional_kwargs['source']}")

    # --- AGENT LOGIC ---
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Agent is reasoning..."):
                try:
                    inputs = {"messages": st.session_state.messages}
                    final_state = agent_app.invoke(inputs)
                    
                    # Detection for citations
                    tools_used = [m.name.replace("_", " ").title() for m in final_state["messages"] if isinstance(m, ToolMessage)]
                    source_tag = ", ".join(list(set(tools_used))) if tools_used else "Internal Knowledge"

                    # Get only the text-based AI response
                    final_response = next((m for m in reversed(final_state["messages"]) if isinstance(m, AIMessage) and m.content.strip()), None)
                    
                    if final_response:
                        final_response.additional_kwargs["source"] = source_tag
                        st.markdown(final_response.content)
                        st.caption(f"📍 Source: {source_tag}")
                        st.session_state.messages.append(final_response)
                except Exception as e:
                    st.error(f"Error: {e}")
