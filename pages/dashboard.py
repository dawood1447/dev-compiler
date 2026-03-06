# pages/dashboard.py

import streamlit as st
import json
import os
from datetime import datetime
from executor import execute_code
from streamlit_ace import st_ace

st.set_page_config(page_title="Dashboard - Compiler", page_icon="⚡", layout="wide")

# --- AUTHENTICATION BOUNCER ---
if not st.session_state.get("authenticated"):
    st.switch_page("app.py")

# --- HIDE NATIVE HEADER & APPLY GLOBAL CSS ---
st.markdown("""
<style>
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
    .stButton > button {
        background: linear-gradient(90deg, #9333ea, #6366f1); color: white; border: none; border-radius: 8px;
        padding: 0.5rem 2rem; font-weight: bold; transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(147, 51, 234, 0.4); color: white; }
    .stTextArea textarea { background-color: #1e293b !important; color: #f8fafc !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
    [data-testid="stMetricValue"] { color: #a78bfa; }
    .ace_editor { border-radius: 10px; border: 1px solid #6366f1; box-shadow: 0 0 15px rgba(99,102,241,0.4); }
</style>
""", unsafe_allow_html=True)

# --- TOP RIGHT PROFILE DROPDOWN ---
head_col1, head_col2 = st.columns([8, 2])
with head_col2:
    st.write("") 
    with st.popover("⚙ Profile ▼", use_container_width=True):
        st.markdown(f"<div style='text-align:center;'><b>👤 {st.session_state.get('username', 'Developer')}</b></div>", unsafe_allow_html=True)
        st.divider()
        st.page_link("pages/settings.py", label="👤 Profile")
        st.page_link("pages/settings.py", label="🎨 Preferences")
        st.page_link("pages/settings.py", label="🛡️ Security")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["authenticated"] = False
            st.switch_page("app.py")

# --- SIDEBAR AVATAR & MENU ---
username = st.session_state.get("username", "Developer")
st.sidebar.markdown(f"""
<div style='text-align: center; margin-top: -20px; margin-bottom: 20px;'>
    <img src='https://api.dicebear.com/9.x/avataaars/svg?seed={username}' width='90' style='border-radius: 50%; border: 2px solid #9333ea;'>
    <h3 style='margin-bottom: 0; color: #f8fafc;'>{username}</h3>
    <p style='color: #94a3b8; font-size: 0.9rem; margin-top: 5px;'>Software Developer</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.page_link("app.py", label="🏠 Welcome Page")
st.sidebar.page_link("pages/dashboard.py", label="💻 Dashboard")
st.sidebar.page_link("pages/history.py", label="📜 Execution History")
st.sidebar.page_link("pages/settings.py", label="⚙ Settings")

# --- HEADER ---
st.markdown("""
<h1 style='text-align:center; background:linear-gradient(90deg,#9333ea,#6366f1); -webkit-background-clip:text; color:transparent; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem;'>
⚡ Online Code Compiler
</h1>
<p style='text-align:center;color:#94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>Run Python code instantly in your browser</p>
""", unsafe_allow_html=True)

# --- 🆕 TEMPLATES LOGIC ---
TEMPLATES = {
    "Custom (Keep my code)": "",
    "Hello World": "print('Hello, World!')",
    "Input Example": "name = input('Enter your name: ')\nprint(f'Hello, {name}! Welcome to the compiler.')",
    "Loop Example": "for i in range(1, 6):\n    print(f'Processing item {i}...')",
    "Math & Functions": "import math\n\ndef calculate_area(radius):\n    return math.pi * (radius ** 2)\n\nprint(f'Area of circle (r=5): {calculate_area(5):.2f}')"
}

def load_template():
    selection = st.session_state.template_dropdown
    if selection != "Custom (Keep my code)":
        st.session_state["code_input"] = TEMPLATES[selection]
        st.session_state["editor_key"] += 1 # Force editor to refresh and show new code

if "editor_key" not in st.session_state: st.session_state["editor_key"] = 0
if "code_input" not in st.session_state: st.session_state["code_input"] = TEMPLATES["Hello World"]

# Selectors above the editor
col_lang, col_temp = st.columns(2)
with col_lang: 
    language = st.selectbox("🐍 Language", ["Python"])
with col_temp: 
    st.selectbox("📝 Code Templates", list(TEMPLATES.keys()), key="template_dropdown", on_change=load_template)

# --- EDITOR ---
code_val = st_ace(
    value=st.session_state["code_input"],
    language=language.lower(),
    theme="dracula",
    keybinding="vscode",
    font_size=15,
    height=350,
    key=f"editor_{st.session_state['editor_key']}"
)
st.session_state["code_input"] = code_val

# --- TOOLBAR ---
t1, t2, t3, t4 = st.columns(4)
with t1: run = st.button("▶ Run Code", use_container_width=True, type="primary")
with t2: 
    if st.button("🧹 Clear", use_container_width=True):
        st.session_state["code_input"] = ""
        st.session_state["editor_key"] += 1
        st.rerun()
with t3: st.download_button("⬇ Download", st.session_state["code_input"], "script.py", use_container_width=True)
with t4: 
    if st.button("📋 Copy", use_container_width=True): st.toast("Press Ctrl+C inside the editor to copy code!", icon="📋")

st.write("### Configuration")
col1, col2 = st.columns(2)
with col1: user_input = st.text_area("📥 Standard Input (stdin)", height=100, placeholder="Type standard input here...")
with col2: timeout_limit = st.slider("⏱️ Runtime Limit (seconds)", 1, 15, 5)

if run:
    with st.spinner("Executing..."):
        output, exec_time, is_error, v_str, memory = execute_code(st.session_state["code_input"], language, user_input, timeout_limit)
        
        # Save History Logic
        history_entry = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "language": language, "version": v_str, "memory": memory, "code": st.session_state["code_input"], "output": output, "exec_time": f"{exec_time:.3f}s", "is_error": is_error}
        history_file = "history.json"
        history = json.load(open(history_file)) if os.path.exists(history_file) else []
        history.append(history_entry)
        json.dump(history, open(history_file, "w"), indent=4)
        
        # Results
        st.markdown("---")
        st.write("### Execution Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("🐍 Language", v_str); m2.metric("⏱ Time", f"{exec_time:.3f}s"); m3.metric("💾 Memory", memory)
        
        st.write("")
        if is_error: st.error("⚠️ Error Detected")
        else: st.success("✅ Success")
        st.markdown("### 🖥 Terminal Output")
        st.code(output, language="bash")

st.markdown("---")
st.caption("⚡ Online Code Compiler | Built by Dawood | 2026")