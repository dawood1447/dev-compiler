# pages/dashboard.py

import streamlit as st
import json
import os
import base64
import zlib
from datetime import datetime
from executor import execute_code
from languages import get_language_config
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
    .stButton > button { background: linear-gradient(90deg, #9333ea, #6366f1); color: white; border: none; border-radius: 8px; padding: 0.5rem 2rem; font-weight: bold; transition: all 0.3s ease; }
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
st.sidebar.markdown(f"<div style='text-align: center; margin-top: -20px; margin-bottom: 20px;'><img src='https://api.dicebear.com/9.x/avataaars/svg?seed={username}' width='90' style='border-radius: 50%; border: 2px solid #9333ea;'><h3 style='margin-bottom: 0; color: #f8fafc;'>{username}</h3><p style='color: #94a3b8; font-size: 0.9rem; margin-top: 5px;'>Software Developer</p></div>", unsafe_allow_html=True)
st.sidebar.page_link("app.py", label="🏠 Welcome Page")
st.sidebar.page_link("pages/dashboard.py", label="💻 Dashboard")
st.sidebar.page_link("pages/history.py", label="📜 Execution History")
st.sidebar.page_link("pages/settings.py", label="⚙ Settings")

st.markdown("<h1 style='text-align:center; background:linear-gradient(90deg,#9333ea,#6366f1); -webkit-background-clip:text; color:transparent; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem;'>⚡ Online Code Compiler</h1><p style='text-align:center;color:#94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>Run multiple languages instantly in your browser</p>", unsafe_allow_html=True)

# --- 🔗 URL SHARE LINK LOADER ---
if "share_code" in st.query_params and "editor_loaded_from_share" not in st.session_state:
    try:
        b64_str = st.query_params["share_code"]
        compressed = base64.urlsafe_b64decode(b64_str.encode('utf-8'))
        decoded_code = zlib.decompress(compressed).decode('utf-8')
        
        st.session_state["code_input"] = decoded_code
        if "share_lang" in st.query_params: st.session_state["share_lang_target"] = st.query_params["share_lang"]
            
        st.session_state["editor_loaded_from_share"] = True
        st.session_state["editor_key"] = st.session_state.get("editor_key", 0) + 1
        st.toast("Shared code loaded successfully!", icon="✅")
    except Exception:
        st.toast("Invalid or corrupted share link.", icon="❌")

# --- 🆕 COMPLETE MULTI-LANGUAGE TEMPLATES ---
LANGUAGE_TEMPLATES = {
    "Python": {
        "Custom (Keep my code)": "",
        "Hello World": "print('Hello, World!')",
        "Input Example": "name = input('Enter your name: ')\nprint(f'Hello, {name}!')",
        "Loop Example": "for i in range(1, 6):\n    print(f'Iteration: {i}')",
        "Math & Functions": "def calculate_square(num):\n    return num * num\n\nprint(f'The square of 5 is: {calculate_square(5)}')\n"
    },
    "C": {
        "Custom (Keep my code)": "",
        "Hello World": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
        "Input Example": "#include <stdio.h>\n\nint main() {\n    char name[50];\n    scanf(\"%49s\", name);\n    printf(\"Hello, %s!\\n\", name);\n    return 0;\n}",
        "Loop Example": "#include <stdio.h>\n\nint main() {\n    for(int i = 1; i <= 5; i++) {\n        printf(\"Iteration: %d\\n\", i);\n    }\n    return 0;\n}",
        "Math & Functions": "#include <stdio.h>\n\nint calculate_square(int num) {\n    return num * num;\n}\n\nint main() {\n    printf(\"The square of 5 is: %d\\n\", calculate_square(5));\n    return 0;\n}"
    },
    "C++": {
        "Custom (Keep my code)": "",
        "Hello World": "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello, World!\" << endl;\n    return 0;\n}",
        "Input Example": "#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string name;\n    cin >> name;\n    cout << \"Hello, \" << name << \"!\" << endl;\n    return 0;\n}",
        "Loop Example": "#include <iostream>\nusing namespace std;\n\nint main() {\n    for(int i = 1; i <= 5; i++) {\n        cout << \"Iteration: \" << i << endl;\n    }\n    return 0;\n}",
        "Math & Functions": "#include <iostream>\nusing namespace std;\n\nint calculate_square(int num) {\n    return num * num;\n}\n\nint main() {\n    cout << \"The square of 5 is: \" << calculate_square(5) << endl;\n    return 0;\n}"
    },
    "Java": {
        "Custom (Keep my code)": "",
        "Hello World": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
        "Input Example": "import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        String name = scanner.nextLine();\n        System.out.println(\"Hello, \" + name + \"!\");\n    }\n}",
        "Loop Example": "public class Main {\n    public static void main(String[] args) {\n        for(int i = 1; i <= 5; i++) {\n            System.out.println(\"Iteration: \" + i);\n        }\n    }\n}",
        "Math & Functions": "public class Main {\n    public static int calculateSquare(int num) {\n        return num * num;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(\"The square of 5 is: \" + calculateSquare(5));\n    }\n}"
    },
    "JavaScript": {
        "Custom (Keep my code)": "",
        "Hello World": "console.log('Hello, World!');",
        "Input Example": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim();\nconsole.log(`Hello, ${input || 'Developer'}!`);",
        "Loop Example": "for (let i = 1; i <= 5; i++) {\n    console.log(`Iteration: ${i}`);\n}",
        "Math & Functions": "function calculateSquare(num) {\n    return num * num;\n}\n\nconsole.log(`The square of 5 is: ${calculateSquare(5)}`);"
    }
}

lang_options = ["Python", "C", "C++", "Java", "JavaScript"]
default_lang_val = st.session_state.get("share_lang_target", "Python")
default_idx = lang_options.index(default_lang_val) if default_lang_val in lang_options else 0

col_lang, col_temp = st.columns(2)
with col_lang: language = st.selectbox("🌐 Language", lang_options, index=default_idx)
current_templates = LANGUAGE_TEMPLATES.get(language, {})
with col_temp: selected_temp = st.selectbox("📝 Code Templates", list(current_templates.keys()), index=1) # Default to 'Hello World'

if st.session_state.get("prev_temp") != selected_temp or st.session_state.get("prev_lang") != language:
    if "editor_loaded_from_share" in st.session_state: 
        del st.session_state["editor_loaded_from_share"]
    else:
        # Only overwrite the code if they didn't select "Custom (Keep my code)"
        if selected_temp != "Custom (Keep my code)":
            st.session_state["code_input"] = current_templates[selected_temp]
            st.session_state["editor_key"] = st.session_state.get("editor_key", 0) + 1
            
    st.session_state["prev_temp"] = selected_temp
    st.session_state["prev_lang"] = language
    st.rerun()

ace_lang_map = {"C": "c_cpp", "C++": "c_cpp", "Java": "java", "JavaScript": "javascript", "Python": "python"}

code_val = st_ace(
    value=st.session_state.get("code_input", "print('Hello, World!')"),
    language=ace_lang_map[language], theme="dracula", keybinding="vscode", font_size=15, height=350,
    key=f"editor_{st.session_state.get('editor_key', 0)}"
)
st.session_state["code_input"] = code_val

# --- UPGRADED 5-BUTTON TOOLBAR ---
t1, t2, t3, t4, t5 = st.columns(5)
with t1: run = st.button("▶ Run Code", use_container_width=True, type="primary")
with t2: 
    if st.button("🧹 Clear", use_container_width=True): 
        st.session_state["code_input"] = ""; st.session_state["editor_key"] += 1; st.rerun()
with t3: st.download_button("⬇ Download", st.session_state["code_input"], f"script.{get_language_config(language)['extension']}", use_container_width=True)
with t4: 
    if st.button("📋 Copy", use_container_width=True): st.toast("Press Ctrl+C inside the editor to copy code!", icon="📋")
with t5:
    if st.button("🔗 Share", use_container_width=True):
        try:
            code_bytes = st.session_state["code_input"].encode('utf-8')
            compressed = zlib.compress(code_bytes)
            b64_str = base64.urlsafe_b64encode(compressed).decode('utf-8')
            base_url = "https://dev-compiler-w54lllepgagm3wjgacassn.streamlit.app/dashboard"
            st.session_state["share_link"] = f"{base_url}?share_lang={language}&share_code={b64_str}"
        except Exception: st.error("Failed to generate link.")

if "share_link" in st.session_state:
    st.info("🔗 **Link generated! Share this URL with anyone:**")
    st.code(st.session_state["share_link"], language="text")

st.write("### Configuration")
col1, col2 = st.columns(2)
with col1: user_input = st.text_area("📥 Standard Input (stdin)", height=100)
with col2: timeout_limit = st.slider("⏱️ Runtime Limit", 1, 15, 5)

if run:
    with st.spinner(f"Compiling and Executing {language}..."):
        output, exec_time, is_error, v_str, memory = execute_code(st.session_state["code_input"], language, user_input, timeout_limit)
        
        history_entry = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "language": language, "version": v_str, "memory": memory, "code": st.session_state["code_input"], "output": output, "exec_time": f"{exec_time:.3f}s", "is_error": is_error}
        history_file = "history.json"
        history = json.load(open(history_file)) if os.path.exists(history_file) else []
        history.append(history_entry)
        json.dump(history, open(history_file, "w"), indent=4)
        
        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("🌐 Language", v_str); m2.metric("⏱ Time", f"{exec_time:.3f}s"); m3.metric("💾 Memory", memory)
        if is_error: st.error("⚠️ Error Detected")
        else: st.success("✅ Success")
        st.markdown("### 🖥 Terminal Output")
        st.code(output, language="bash")

st.markdown("---")
st.caption("⚡ Online Code Compiler | Built by Dawood | 2026")