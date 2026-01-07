import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Master Aesthetic (High Contrast, Layered Dark Mode, & Identity Icons)
st.markdown("""
    <style>
    /* 1. CLEANUP & BASE THEME */
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    .stApp { 
        background-color: #131314; 
        color: #FFFFFF !important; 
        font-family: 'Segoe UI', sans-serif;
    }

    /* 2. SIDEBAR & SELECTBOX */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        border: 1px solid #444 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="popover"] { background-color: transparent !important; }
    ul[data-testid="stSelectboxVirtualList"] {
        background-color: #262730 !important;
        border: 1px solid #444 !important;
    }
    div[role="option"] { background-color: #262730 !important; color: #FFFFFF !important; }
    div[role="option"]:hover { background-color: #3D3E47 !important; color: #A5D8FF !important; }

    /* 3. CHAT INPUT FIX (Pure White on Dark Grey) */
    .stChatInputContainer { background-color: transparent !important; border: none !important; }
    .stChatInputContainer textarea {
        background-color: #1E1F20 !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
        border-radius: 28px !important;
        padding: 12px 20px !important;
    }
    .stChatInputContainer p { color: #888 !important; }

    /* 4. IDENTITY ICONS: KLUE PENTAGON (CSS RENDERED) */
    .klue-icon {
        width: 32px; height: 32px; border-radius: 50%;
        border: 2px solid #A5D8FF; position: relative; 
        display: flex; justify-content: center; align-items: center; 
        background: #131314; margin-right: 10px;
    }
    .pip { width: 5px; height: 5px; border-radius: 50%; position: absolute; }
    .pip-1 { background: #00A67E; top: 4px; }               /* OpenAI */
    .pip-2 { background: #D97757; top: 12px; left: 4px; }    /* Anthropic */
    .pip-3 { background: #4285F4; bottom: 6px; left: 7px; }  /* Google */
    .pip-4 { background: #0668E1; bottom: 6px; right: 7px; } /* Meta */
    .pip-5 { background: #FF9000; top: 12px; right: 4px; }   /* Mistral */

    /* 5. IDENTITY ICONS: USER RING */
    .user-icon {
        width: 30px; height: 30px; border-radius: 50%;
        border: 2px solid #8E9EAB; background: transparent;
        margin-right: 10px;
    }

    /* 6. STATUS BOXES (ICE BLUE) */
    .status-base {
        color: #A5D8FF !important;
        border: 1px solid #A5D8FF !important;
        padding: 12px; border-radius: 8px; font-size: 0.85rem;
        font-weight: 700; text-align: center; letter-spacing: 2px; margin-top: 10px;
    }
    .status-lite { background-color: rgba(165, 216, 255, 0.05); }
    .status-pro {
        background-color: rgba(165, 216, 255, 0.1);
        box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4);
        border: 2px solid #A5D8FF !important;
    }
    .status-meta {
        background: linear-gradient(90deg, rgba(165,216,255,0.1) 0%, rgba(165,216,255,0.4) 50%, rgba(165,216,255,0.1) 100%);
        background-size: 200% auto;
        box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6);
        border: 2px solid #FFFFFF !important;
        animation: shimmer 4s linear infinite;
    }
    @keyframes shimmer { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }
    
    .sidebar-footer {
        color: #FFFFFF !important;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    core_specs = (
        "LITE: 2 CORES (Speed)\n"
        "Rapid creative flow. Best for brainstorming.\n\n"
        "PRO: 4 CORES (Logic)\n"
        "Deep logic. Best for verified insights.\n\n"
        "META: 5 CORES (Mastery)\n"
        "Master synthesis. Best for high-stakes accuracy."
    )
    st.markdown("### ENGINE SELECTION", help=core_specs)
    selected_mode = st.selectbox("MODE", ["Lite", "Pro", "Meta"], index=1, label_visibility="collapsed")
    st.markdown("---")
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base status-lite'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-footer'>KLUE | COMBINED INTELLIGENCE</div>", unsafe_allow_html=True)

# 4. Branding Header
st.markdown("<div style='text-align:center; padding: 40px 0;'><h1 style='letter-spacing:15px; font-weight:800; color:white; margin-bottom:0;'>KLUE</h1><p style='letter-spacing:8px; text-transform:uppercase; font-size:0.8rem; color:#A5D8FF;'>Unified AI</p></div>", unsafe_allow_html=True)

# 5. API Client
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("API Key Missing in .streamlit/secrets.toml")
    st.stop()

# 6. Chat History & Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom Message Display
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        icon = "<div class='klue-icon'><div class='pip pip-1'></div><div class='pip pip-2'></div><div class='pip pip-3'></div><div class='pip pip-4'></div><div class='pip pip-5'></div></div>"
    else:
        icon = "<div class='user-icon'></div>"
    
    with st.chat_message(msg["role"], avatar=None):
        st.markdown(f"<div style='display:flex; align-items:flex-start; gap:15px;'>{icon}<div style='padding-top:4px;'>{msg['content']}</div></div>", unsafe_allow_html=True)

# 7. Execution Loop
if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Processing Logic (Triggered after rerun to keep UI clean)
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    user_query = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar=None):
        placeholder = st.empty()
        placeholder.markdown("`[SYNTESIZING FROM MULTIPLE CORES...]`")
        
        # Determine Model Stack
        if selected_mode == "Lite": models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro": models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else: models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        # Parallel Execution (Simplified)
        responses = []
        for m in models:
            try:
                r = client.chat.completions.create(model=m, messages=[{"role": "user", "content": user_query}], max_tokens=500)
                responses.append(r.choices[0].message.content)
            except: pass
        
        # Master Synthesis
        final = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive, no-fluff synthesis of the following data. Combined Intelligence, Unified AI."},
                {"role": "user", "content": f"Core Responses: {responses}. Original Query: {user_query}"}
            ]
        )
        
        ans = final.choices[0].message.content
        placeholder.markdown(f"<div style='display:flex; align-items:flex-start; gap:15px;'><div class='klue-icon'><div class='pip pip-1'></div><div class='pip pip-2'></div><div class='pip pip-3'></div><div class='pip pip-4'></div><div class='pip pip-5'></div></div><div style='padding-top:4px;'>{ans}</div></div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": ans})
