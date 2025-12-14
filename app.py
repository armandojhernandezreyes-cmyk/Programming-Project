from llm_utils import summarize_text, chatbot_reply
import streamlit as st
from db import create_tables
from auth_ui import login_ui, signup_ui, forgot_password_ui

create_tables()


def has_google_user() -> bool:
    """
    Streamlit sets st.user when OIDC is enabled.
    We treat the user as logged in only if st.user exists AND is_logged_in is True.
    """
    u = getattr(st, "user", None)
    return bool(u) and getattr(u, "is_logged_in", False)


def main():
    st.title("Login System with SQLite")

    # --------------------------
    # Session state initialization
    # --------------------------
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "just_logged_out" not in st.session_state:
        st.session_state["just_logged_out"] = False

    # If Google session is gone, allow Google login buttons to behave normally
    if not has_google_user():
        st.session_state["just_logged_out"] = False

    # --------------------------
    # Authentication Section
    # --------------------------
    if st.session_state["user"] is None:
        option = st.radio("Select an option:", ["Login", "Sign up", "Forgot password"])

        if option == "Login":
            login_ui()
        elif option == "Sign up":
            signup_ui()
        else:
            forgot_password_ui()

    # --------------------------
    # Main App (After Login)
    # --------------------------
    else:
        st.success(f"Welcome, {st.session_state['user']}!")

        tab_summary, tab_chat = st.tabs(["Summarizer", "Chatbot"])

        # ---- Summarizer ----
        with tab_summary:
            st.subheader("AI Text Summarizer")
            user_text = st.text_area("Write or paste text to summarize:")

            if st.button("Summarize"):
                if user_text.strip():
                    summary = summarize_text(user_text)
                    st.subheader("Summary:")
                    st.write(summary)
                else:
                    st.warning("Please enter some text to summarize.")

        # ---- Chatbot ----
        with tab_chat:
            st.subheader("Programming Tutor Chatbot")

            if st.session_state["chat_history"]:
                for msg in st.session_state["chat_history"]:
                    if msg["role"] == "user":
                        st.markdown(f"**You:** {msg['content']}")
                    else:
                        st.markdown(f"**Tutor:** {msg['content']}")
            else:
                st.info("Start the conversation by asking a question below.")

            user_message = st.text_input(
                "Type your question here:",
                key="chat_input",
                placeholder="For example: Explain Python loops, or how SQLite stores users.",
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Send", key="send_chat"):
                    if user_message.strip():
                        st.session_state["chat_history"].append(
                            {"role": "user", "content": user_message.strip()}
                        )
                        reply = chatbot_reply(st.session_state["chat_history"])
                        st.session_state["chat_history"].append(
                            {"role": "assistant", "content": reply}
                        )
                        st.rerun()
                    else:
                        st.warning("Please type a message before sending.")

            with col2:
                if st.button("Clear chat", key="clear_chat"):
                    st.session_state["chat_history"] = []
                    st.rerun()

        # ---- Logout ----
        if st.button("Logout"):
            st.session_state["user"] = None
            st.session_state["just_logged_out"] = True

            # If logged in via Google (OIDC), also logout of Streamlit auth
            if has_google_user():
                st.logout()

            st.rerun()


if __name__ == "__main__":
    main()
