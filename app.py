import streamlit as st
from services.agent import run_agent

# Page configuration
st.set_page_config(
    page_title="Tool Calling AI Chatbot",
    page_icon="🤖"
    # layout="centered"
)

# Application title
st.title("🤖 Tool Calling AI Chatbot")
st.caption("Your AI assistant powered by Python")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("Ask me anything..."):

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = run_agent(st.session_state.messages)

                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                st.error(f"Error: {e}")