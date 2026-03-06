# pages/settings.py

import streamlit as st

st.set_page_config(page_title="Settings - Compiler", page_icon="⚙️", layout="wide")

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")

st.markdown("""<style> [data-testid="stHeader"] { display: none !important; } [data-testid="stSidebarNav"] { display: none !important; } .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); } </style>""", unsafe_allow_html=True)

# TOP RIGHT MENU
head_col1, head_col2 = st.columns([8, 2])
with head_col2:
    with st.popover("⚙ Profile ▼", use_container_width=True):
        st.markdown(f"<div style='text-align:center;'><b>👤 {st.session_state.get('username', 'Developer')}</b></div>", unsafe_allow_html=True)
        st.divider()
        st.page_link("pages/settings.py", label="👤 Profile"); st.page_link("pages/settings.py", label="🎨 Preferences"); st.page_link("pages/settings.py", label="🛡️ Security")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["authenticated"] = False
            st.switch_page("app.py")

# SIDEBAR
username = st.session_state.get("username", "Developer")
st.sidebar.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><img src='https://api.dicebear.com/9.x/avataaars/svg?seed={username}' width='90' style='border-radius: 50%; border: 2px solid #9333ea;'><h3 style='color: white;'>{username}</h3></div>", unsafe_allow_html=True)
st.sidebar.page_link("app.py", label="🏠 Welcome Page"); st.sidebar.page_link("pages/dashboard.py", label="💻 Dashboard"); st.sidebar.page_link("pages/history.py", label="📜 Execution History"); st.sidebar.page_link("pages/settings.py", label="⚙ Settings")

st.markdown("<h1 style='color:white;'>⚙️ Settings</h1>", unsafe_allow_html=True)
t_prof, t_pref, t_sec = st.tabs(["👤 Profile", "🎨 Preferences", "🛡️ Security"])

with t_prof:
    st.write("### Profile Information")
    st.text_input("Username", value=username, disabled=True)
    st.text_input("Email", placeholder="yourname@dev.com")
    st.button("Update Profile")

with t_pref:
    st.write("### Appearance")
    st.selectbox("Editor Theme", ["Dracula", "Monokai", "GitHub Dark"])
    st.slider("Font Size", 12, 24, 15)
    st.button("Save Preferences")

with t_sec:
    st.write("### Security")
    st.text_input("New Password", type="password")
    if st.button("Delete Account", type="primary"): st.error("Account deletion is permanent.")

st.markdown("---")
st.caption("⚡ Online Code Compiler | Built by Dawood | 2026")