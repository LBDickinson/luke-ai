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

# 2. MASTER AESTHETIC ENGINE (Complete UI Overhaul)
st.markdown("""
    <style>
    /* 1. HIDING DEFAULT OVERLAYS */
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}
    
    /* 2. GLOBAL THEME: PURE WHITE & DEEP DARK */
    .stApp { 
        background-color: #131314; 
        color: #FFFFFF !important; 
        font-family: 'Segoe UI', sans-serif;
    }

    /* 3. SIDEBAR: HIGH CONTRAST DARK MODE */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    
    /* Ensuring sidebar text is forced to white */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    
    /* 4. SELECTOR FIX: SOLVING WHITE-ON-WHITE */
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        border: 1px solid #444 !important;
        color: #FFFFFF !important;
    }

    /* Target the dropdown popover (the menu that appears after clicking) */
    div[data-baseweb="popover"] {
        background-color: transparent !important;
    }
    ul[data-testid="stSelectboxVirtualList"] {
        background-color: #262730 !important;
        border: 1px solid #444 !important;
    }
    div[role="option"] {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }
    div[role="option"]:hover {
        background-color: #3D3E47 !important;
        color: #A5D8FF !important;
    }

    /* 5. CHAT INPUT: PURE WHITE ON CHARCOAL PILL */
    .stChatInputContainer {
        background-color: transparent !important;
    }
    .stChatInputContainer textarea {
        background-color: #1E1F20 !important;
        color: #FFFFFF !important;
        border: 1px solid #555 !important;
        border-radius: 28px !important;
        padding-left: 20px !important;
    }
    .stChatInputContainer p {
        color: #999 !important; /* Placeholder text */
    }

    /* 6. LOGO: SHINING TITANIUM SHIELD */
    .branding-container { 
        text-align: center; 
        margin-bottom: 50px; 
        padding-top: 20px;
    }
    .logo {
        font-size: 3.2rem; 
        font-weight: 800; 
        letter-spacing: 12px; 
        display: inline-block;
        padding: 15px 35px; 
        background: linear-gradient(135deg, #8E9EAB 0%, #FFFFFF 50%, #8E9EAB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        border: 2px solid #555;
        border-bottom-left-radius: 45px; 
        filter: drop-shadow(4px 4px 10px rgba(0,0,0,0.6));
        animation: logo-shine 8s linear infinite;
    }
    @keyframes logo-shine { to { background-position: 200% center; } }
    .tagline { 
        color: #FFFFFF !important; 
        font-size: 0.8rem; 
        letter-spacing: 10px; 
        margin-top: 25px; 
        text-transform: uppercase; 
        font-weight: 400; 
    }

    /* 7. CORE STATUS BOXES (ICE BLUE) */
    .status-base {
        color: #A5D8FF !important;
        border: 1px solid #A5D8FF !important;
        padding: 12px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
        text-align: center;
        letter-spacing: 2px;
        margin-top: 15px;
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
        margin-top: 40px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: CORE SELECTION & DESCRIPTORS
with st.sidebar:
    # UPDATED DESCRIPTORS FROM CONVERSATION
    core_specs = (
        "**LITE: 2 CORES**\nOptimized for rapid creative flow. Best for brainstorming and quick Q&A.\n\n"
        "**PRO: 4 CORES**\nBalanced for deep logic. Best for verified insights and complex reasoning.\n\n"
        "**META: 5 CORES**\nFull-power master synthesis. Best for high-stakes accuracy and definitive results."
    )
    
    st.markdown("### ENGINE SELECTION", help=core_specs)
    
    selected_mode = st.selectbox(
        "CORE SELECTION",
        ["Lite", "Pro", "Meta"],
        index=1,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # DYNAMIC BOX UPDATES
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base status-lite'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-footer'>KLUE | COMBINED INTELLIGENCE</div>", unsafe_allow_html=True)

# 4. BRANDING HEADER
st.markdown("""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='tagline'>Unified AI</div>
    </div>
    """, unsafe_allow_html=True)

# 5. OPENROUTER API LOGIC
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"]
    )
except Exception:
    st.error("API Key Missing in Secrets.")
    st.stop()

# 6. CHAT SESSION ENGINE
if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY HISTORY WITH TITANIUM/ICE-BLUE THEME
for message in st.session_state.messages:
    avatar_choice = "🔘" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_choice):
        st.markdown(message["content"])

# 7. MASTER SOURCE EXECUTION LOOP
if prompt := st.chat_input("Command the Master Source..."):
    # 1. Store and display user command
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Engage Synthesis
    with st.chat_message("assistant", avatar="🔘"):
        status_area = st.empty()
        status_area.markdown("`[SYSTEM: MERGING CORES...]`")
        
        # Determine Core Stack
        if selected_mode == "Lite":
            cores = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro":
            cores = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else:
            cores = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        # Parallel Execution
        core_data = []
        for core_id in cores:
            try:
                core_res = client.chat.completions.create(
                    model=core_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=600
                )
                core_data.append(core_res.choices[0].message.content)
            except Exception:
                continue

        # Master Synthesis Core
        master_synthesis = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive synthesis of the following intelligence cores. Unified AI format. No fluff."},
                {"role": "user", "content": f"Intelligence Cores: {core_data}. Query: {prompt}"}
            ]
        )
        
        final_result = master_synthesis.choices[0].message.content
        status_area.markdown(final_result)
        st.session_state.messages.append({"role": "assistant", "content": final_result})
