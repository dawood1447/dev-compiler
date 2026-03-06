# pages/history.py

import streamlit as st
import json
import os

st.set_page_config(page_title="History - Compiler", page_icon="🕰️", layout="wide")

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

st.title("🕰️ Execution History")
history_file = "history.json"

if os.path.exists(history_file):
    history = json.load(open(history_file))
    if not history: st.info("History is empty.")
    else:
        if st.button("🗑️ Clear All History", use_container_width=True):
            json.dump([], open(history_file, "w")); st.rerun()
        for entry in reversed(history):
            with st.expander(f"{'❌' if entry.get('is_error', False) else '✅'} {entry.get('timestamp', 'Unknown Time')} - {entry.get('language', 'Python')}"):
                
                # --- THE FIX: Safely get values using .get() with defaults ---
                v_str = entry.get('version', '')
                t_str = entry.get('exec_time', 'N/A')
                m_str = entry.get('memory', 'N/A')
                
                st.info(f"🐍 {entry.get('language', 'Python')} {v_str} | ⏱ {t_str} | 💾 {m_str}")
                # -------------------------------------------------------------
                
                st.write("**Code:**")
                st.code(entry.get('code', ''), language="python")
                
                st.write("**Output:**")
                st.code(entry.get('output', ''), language="bash")
else: st.info("No history found.")

st.markdown("---")
st.caption("⚡ Online Code Compiler | Built by Dawood | 2026")