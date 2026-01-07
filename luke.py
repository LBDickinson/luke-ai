import streamlit as st
from openai import OpenAI
import time

# 1. SYSTEM CONFIGURATION
st.set_page_config(
    page_title="KLUE | Unified AI",
    page_icon="🔘",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. MASTER AESTHETIC ENGINE (v7.3 - Ice Blue Identity)
st.markdown("""
    <style>
    /* 1. INTERFACE CLEANUP */
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}
    
    /* 2. GLOBAL THEME & TITANIUM TEXT */
    .stApp { 
        background-color: #131314; 
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* CHAT TEXT: Soft Titanium White (#F0F2F5) */
    [data-testid="stChatMessageContent"] p {
        color: #F0F2F5 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* 3. ICON STYLING: ICE BLUE FOR KLUE */
    /* This targets the Material Symbol for the Assistant only */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {
        color: #A5D8FF !important;
    }
    
    /* 4. SIDEBAR: HIGH-CONTRAST CONTROL PANEL */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        letter-spacing: 2px !important;
        text-transform: uppercase;
        font-size: 0.9rem !important;
        font-weight: 800 !important;
    }

    [data-testid="stSidebar"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    
    /* 5. SELECTOR MENU: DARK SURFACES */
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        border: 1px solid #444 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="popover"] { background-color: #262730 !important; }
    div[role="option"] { background-color: #262730 !important; color: #FFFFFF !important; }
    div[role="option"]:hover { background-color: #3D3E47 !important; color: #A5D8FF !important; }

    /* 6. CHAT INPUT: INTEGRATED DARK DESIGN */
    .stChatInputContainer textarea {
        background-color: #1E1F20 !important;
        color: #F0F2F5 !important;
        border: 1px solid #555 !important;
        border-radius: 28px !important;
    }

    /* 7. LOGO: TITANIUM SHINE */
    .branding-container { text-align: center; margin-bottom: 50px; padding-top: 20px; }
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
        padding: 15px 35px; 
        background: linear-gradient(135deg, #8E9EAB 0%, #FFFFFF 50%, #8E9EAB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        border: 2px solid #555; border-bottom-left-radius: 45px; 
        filter: drop-shadow(4px 4px 10px rgba(0,0,0,0.6));
        animation: logo-shine 8s linear infinite;
    }
    @keyframes logo-shine { to { background-position: 200% center; } }
    .tagline { color: #FFFFFF !important; font-size: 0.8rem; letter-spacing: 10px; margin-top: 25px; text-transform: uppercase; }

    /* 8. CORE STATUS BOXES */
    .status-base {
        color: #A5D8FF !important; border: 1px solid #A5D8FF !important;
        padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 700;
        text-align: center; letter-spacing: 2px; margin-top: 15px;
    }
    .status-pro { box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4); border: 2px solid #A5D8FF !important; }
    .status-meta { border: 2px solid #FFFFFF !important; box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6); }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: OPERATING CORE SELECTION
with st.sidebar:
    core_specs = (
        "**LITE: 2 CORES**\nOptimized for rapid creative flow. Best for brainstorming and quick Q&A.\n\n"
        "**PRO: 4 CORES**\nBalanced for deep logic. Best for verified insights and complex reasoning.\n\n"
        "**META: 5 CORES**\nFull-power master synthesis. Best for high-stakes accuracy and definitive results."
    )
    
    st.markdown("### Engine Selection", help=core_specs)
    selected_mode = st.selectbox("CORE SELECTION", ["Lite", "Pro", "Meta"], index=1, label_visibility="collapsed")
    st.markdown("---")
    
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)

# 4. BRANDING HEADER
st.markdown("<div class='branding-container'><div class='logo'>KLUE</div><div class='tagline'>Unified AI</div></div>", unsafe_allow_html=True)

# 5. OPENROUTER CLIENT
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("API Key Missing in Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. CHAT DISPLAY (Ice Blue Hub & Pulse)
for message in st.session_state.messages:
    # KLUE = hub, User = radio_button_checked (The Pulse)
    avatar_icon = ":material/hub:" if message["role"] == "assistant" else ":material/radio_button_checked:"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 7. EXECUTION
if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/radio_button_checked:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=":material/hub:"):
        status_area = st.empty()
        status_area.markdown("`[SYSTEM: MERGING CORES...]`")
        
        if selected_mode == "Lite": cores = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro": cores = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else: cores = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        core_outputs = []
        for c in cores:
            try:
                res = client.chat.completions.create(model=c, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                core_outputs.append(res.choices[0].message.content)
            except: continue

        master = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive synthesis. Master intelligence mode."},
                {"role": "user", "content": f"Intelligence Data: {core_outputs}. Command: {prompt}"}
            ]
        )
        
        ans = master.choices[0].message.content
        status_area.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
