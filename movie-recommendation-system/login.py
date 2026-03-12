import streamlit as st
from auth import create_user_table, add_user, login_user

def login_signup_screen():
    create_user_table()

    menu = ["Login", "Signup"]
    choice = st.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if login_user(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()

            else:
                st.error("Incorrect Username or Password")

    elif choice == "Signup":
        st.subheader("Create a New Account")
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        if st.button("Signup"):
            try:
                add_user(new_user, new_password)
                st.success("Signup successful! You can login now.")
            except:
                st.error("Username already exists!")
