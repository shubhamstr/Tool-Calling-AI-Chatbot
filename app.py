
import streamlit as st

from services.agent import run_agent
from services.email_service import send_email


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Tool Calling AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------
# Application Header
# --------------------------------

st.title("🤖 Tool Calling AI Chatbot")
st.caption("Your AI assistant powered by Python")


# --------------------------------
# Session State Initialization
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_email" not in st.session_state:
    st.session_state.pending_email = None


# --------------------------------
# Display Chat History
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------
# Chat Input
# --------------------------------

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

                result = run_agent(
                    st.session_state.messages
                )

                response = result["response"]
                pending_email = result["pending_email"]

                # Display AI response
                st.markdown(response)

                # Save pending email
                if pending_email:
                    st.session_state.pending_email = pending_email

                # Store assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                st.error(f"Error: {e}")


# --------------------------------
# Email Confirmation Interface
# --------------------------------

if st.session_state.pending_email:

    email = st.session_state.pending_email

    st.divider()

    st.subheader("📧 Email Preview")

    st.warning(
        "Review the email details before sending. "
        "You can edit the fields below."
    )

    draft_id = email["draft_id"]

    # --------------------------------
    # Email Fields
    # --------------------------------

    recipient = st.text_input(
        "Recipient Email",
        value=email["recipient"],
        key=f"recipient_{draft_id}"
    )

    subject = st.text_input(
        "Email Subject",
        value=email["subject"],
        key=f"subject_{draft_id}"
    )

    body = st.text_area(
        "Email Body",
        value=email["body"],
        height=250,
        key=f"body_{draft_id}"
    )

    # --------------------------------
    # Action Buttons
    # --------------------------------

    col1, col2 = st.columns(2)

    # Confirm & Send
    with col1:

        if st.button(
            "✅ Confirm & Send",
            use_container_width=True,
            type="primary"
        ):

            if not recipient.strip():

                st.error("Recipient email is required.")

            elif not subject.strip():

                st.error("Email subject is required.")

            elif not body.strip():

                st.error("Email body is required.")

            else:

                try:

                    with st.spinner("Sending email..."):

                        result = send_email(
                            recipient=recipient.strip(),
                            subject=subject.strip(),
                            body=body.strip()
                        )

                    # Clear pending email
                    st.session_state.pending_email = None

                    # Save successful result
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": (
                            "✅ **Email sent successfully!**\n\n"
                            f"**Recipient:** {recipient}\n\n"
                            f"**Subject:** {subject}\n\n"
                            f"**Email ID:** `{result['email_id']}`"
                        )
                    })

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Failed to send email: {e}"
                    )

    # Cancel Email
    with col2:

        if st.button(
            "❌ Cancel",
            use_container_width=True
        ):

            st.session_state.pending_email = None

            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "Email cancelled. "
                    "No email was sent."
                )
            })

            st.rerun()
