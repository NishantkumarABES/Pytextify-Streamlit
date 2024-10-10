import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import bcrypt
from sqlalchemy import create_engine
from pytextify import main_app

# Create a SQLite Database connection
conn = sqlite3.connect('pytextify_users.db', check_same_thread=False)
c = conn.cursor()

# Create a table to store users if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                name TEXT,
                password TEXT
            )''')
conn.commit()

# Sign Up function to add new users to the database
def add_user(username, name, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute('INSERT INTO users (username, name, password) VALUES (?, ?, ?)', (username, name, hashed_password))
    conn.commit()

# Function to check if the username already exists
def check_user(username):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    return c.fetchone()

# Function to authenticate user on login
def authenticate_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    if user: return bcrypt.checkpw(password.encode(), user[3])
    return False



st.set_page_config(page_title="PyTextify - login & Sign Up", layout="wide", page_icon=":material/login:")


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Streamlit app layout
    col1, col2 = st.columns([0.5, 4])
    with col1: st.image(r"images/logo_path.png", width=100)
    with col2: st.title('PyTextify - Login & Sign Up')
    
    with st.container():
        tab1, tab2 = st.tabs(["Sign Up", "Login"])
        with tab1:
            st.subheader("Create New Account")
            new_user = st.text_input("Username", key='1')
            name = st.text_input("Name")
            col_left , col_right  = st.columns([1, 1])
            with col_left: new_password = st.text_input("Password", type='password', key='2')
            with col_right: confirm_password = st.text_input("Confirm Password", type='password')
            if st.button("Sign Up"):
                if new_password == confirm_password:
                    if check_user(new_user) is None:
                        add_user(new_user, name, new_password)
                        st.success("You have successfully created an account!")
                        st.info("Go to the Login Menu to login")
                    else:
                        st.error("Username already exists! Try a different one.")
                else:
                    st.error("Passwords do not match")
        with tab2:
            st.subheader("Login to PyTextify")
            username = st.text_input("Username", key='3')
            password = st.text_input("Password", type='password', key='4')
            
            if st.button("Login"):
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else: st.error("Incorrect username or password")
        conn.close()
else: main_app()
