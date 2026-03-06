# app.py

import streamlit as st
from auth import create_user, authenticate_user

st.set_page_config(page_title="Welcome - Compiler", page_icon="⚡", layout="wide")

# Initialize Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# Global CSS to hide default nav and style the app
st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none !important; }
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
    .stButton > button {
        background: linear-gradient(90deg, #9333ea, #6366f1);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 2rem; font-weight: bold; transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 4px 12px rgba(147, 51, 234, 0.4); color: white;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# NOT AUTHENTICATED: Show Login / Signup UI
# -----------------------------------------
if not st.session_state["authenticated"]:
    st.markdown("""
    <h1 style='text-align:center; background:linear-gradient(90deg,#9333ea,#6366f1); -webkit-background-clip:text; color:transparent; font-size: 4rem; font-weight: 800; margin-bottom: 0.5rem;'>
    ⚡ Dev Compiler
    </h1>
    <p style='text-align:center;color:#94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>
    Login or Signup to access the ultimate execution environment
    </p>
    """, unsafe_allow_html=True)

    # Use columns to center the login box
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.write("### Welcome Back")
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", use_container_width=True):
                if authenticate_user(login_user, login_pass):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = login_user
                    st.rerun() # Refresh the page instantly
                else:
                    st.error("Invalid username or password.")
                    
        with tab2:
            st.write("### Create an Account")
            new_user = st.text_input("New Username", key="new_user")
            new_pass = st.text_input("New Password", type="password", key="new_pass")
            
            if st.button("Sign Up", use_container_width=True):
                if new_user and new_pass:
                    if create_user(new_user, new_pass):
                        st.success("Account created successfully! Please switch to the Login tab.")
                    else:
                        st.error("Username already exists. Please choose another one.")
                else:
                    st.warning("Please fill in both fields.")

# -----------------------------------------
# AUTHENTICATED: Show Dashboard Access
# -----------------------------------------
else:
    # Custom Sidebar (Only visible when logged in!)
    st.sidebar.title("⚡ Dev Compiler")
    st.sidebar.write(f"👤 **Logged in as:** {st.session_state['username']}")
    st.sidebar.markdown("---")
    st.sidebar.page_link("app.py", label="🏠 Welcome Page")
    st.sidebar.page_link("pages/dashboard.py", label="💻 Dashboard")
    st.sidebar.page_link("pages/history.py", label="📜 Execution History")
    st.sidebar.page_link("pages/settings.py", label="⚙ Settings")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()

    # Welcome Page Content
    st.markdown("""
    <h1 style='text-align:center; background:linear-gradient(90deg,#9333ea,#6366f1); -webkit-background-clip:text; color:transparent; font-size: 4rem; font-weight: 800; margin-bottom: 0.5rem;'>
    ⚡ Dev Compiler
    </h1>
    <p style='text-align:center;color:#94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>
    The Ultimate Online Execution Environment
    </p>
    """, unsafe_allow_html=True)

    st.success(f"Welcome to your workspace, {st.session_state['username']}!")
    
    st.markdown("""
    ### 🚀 Getting Started
    Navigate using the custom sidebar on the left:
    * **💻 Dashboard:** Write, input, and execute your code.
    * **📜 Execution History:** Review your past code runs and metrics.
    
    👈 **Select 'Dashboard' to start coding!**
    """)

st.markdown("---")
st.caption("⚡ Online Code Compiler | Built by Dawood | 2026")