import streamlit as st
import bcrypt
from db import create_user, get_user_by_email, update_user_password


# -------------------------------
# Password hashing helpers
# -------------------------------
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# -------------------------------
# Sign-up UI
# -------------------------------
def signup_ui():
    st.subheader("Sign up")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password2 = st.text_input("Repeat Password", type="password")
        create_btn = st.form_submit_button("Create account")

    if create_btn:
        if not email.strip() or not password or not password2:
            st.error("Please fill in all fields.")
            return

        if password != password2:
            st.error("Passwords do not match.")
            return

        password_hash = hash_password(password)
        success = create_user(email.strip(), password_hash)

        if success:
            st.success("Account created! You can now log in.")
        else:
            st.error("This email is already registered.")


# -------------------------------
# Login UI
# -------------------------------
def login_ui():
    st.subheader("Login")

    # -------- Email + password login --------
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if not email.strip() or not password:
            st.error("Please fill in all fields.")
            return

        user = get_user_by_email(email.strip())
        if user is None:
            st.error("User not found. Please sign up first.")
            return

        stored_hash = user[2]
        if check_password(password, stored_hash):
            st.session_state["user"] = email.strip()
            st.session_state["just_logged_out"] = False
            st.success("Logged in successfully.")
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.markdown("---")

    # -------- Google login (ONLY for registered users) --------
    st.write("Or sign in using Google (registered users only):")

    # Prevent rerun loops by checking once per page load
    if "google_gate_checked" not in st.session_state:
        st.session_state["google_gate_checked"] = False

    if getattr(st, "user", None) is not None and st.user.is_logged_in:
        google_email = getattr(st.user, "email", None)

        if not google_email:
            st.error("Google login did not return an email address. Please try again.")
            if st.button("Logout Google"):
                st.logout()
                st.session_state["google_gate_checked"] = False
                st.rerun()
            return

        # Gate access: only allow if email exists in SQLite
        db_user = get_user_by_email(google_email)

        if db_user is None:
            st.error(
                "This Google account is not registered in the system. "
                "Please sign up first using the same email, then log in."
            )

            # Let them clear the Google session easily
            if st.button("Logout Google"):
                st.logout()
                st.session_state["google_gate_checked"] = False
                st.rerun()

            return

        # If registered, auto-enter the app (only once to avoid loops)
        if not st.session_state["google_gate_checked"]:
            st.session_state["google_gate_checked"] = True
            st.session_state["user"] = google_email
            st.session_state["just_logged_out"] = False
            st.rerun()

    # If not logged in with Google, show sign-in button
    if st.button("Sign in with Google"):
        st.session_state["just_logged_out"] = False
        st.session_state["google_gate_checked"] = False
        st.login("google")


# -------------------------------
# Forgot Password UI
# -------------------------------
def forgot_password_ui():
    st.subheader("Forgot password")
    st.info("Enter the email you used to sign up and choose a new password.")

    with st.form("reset_form"):
        email = st.text_input("Email")
        new_password = st.text_input("New password", type="password")
        new_password2 = st.text_input("Repeat new password", type="password")
        reset_btn = st.form_submit_button("Reset password")

    if reset_btn:
        if not email.strip() or not new_password or not new_password2:
            st.error("Please fill in all fields.")
            return

        if new_password != new_password2:
            st.error("New passwords do not match.")
            return

        user = get_user_by_email(email.strip())
        if user is None:
            st.error("No user found with that email.")
            return

        new_hash = hash_password(new_password)
        ok = update_user_password(email.strip(), new_hash)

        if ok:
            st.success("Password updated! You can now log in.")
        else:
            st.error("Something went wrong while updating the password.")
