import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Tool Calling AI Chatbot",
    page_icon="🤖",
    layout="centered"
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

    # Temporary response (we'll integrate AI later)
    response = f"You said: {prompt}"

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)