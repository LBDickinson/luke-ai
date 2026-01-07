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

# 2. MASTER AESTHETIC (The full CSS Engine)
st.markdown("""
    <style>
    /* 1. CLEANUP & HIDING DEFAULT OVERLAYS */
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}
    
    /* 2. GLOBAL THEME (Pure White & Deep Charcoal) */
    .stApp { 
        background-color: #131314; 
        color: #FFFFFF !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 3. SIDEBAR: HIGH CONTRAST DARK MODE */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    
    /* Force Sidebar labels and captions to Bright White */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    
    /* 4. SELECTBOX DROPDOWN: PREVENTING WHITE-ON-WHITE */
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        border: 1px solid #444 !important;
        color: #FFFFFF !important;
    }

    /* Dropdown Popover List Styling */
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

    /* 5. CHAT INPUT: PURE WHITE ON DARK GREY */
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
        color: #999 !important; /* Placeholder color */
    }

    /* 6. BRAND LOGO: SHINING TITANIUM SHIELD */
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

    /* 7. CORE STATUS INDICATORS */
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

# 3. SIDEBAR: OPERATING CORE SELECTION
with st.sidebar:
    # DEFINING THE CORE SPECS TOOLTIP
    core_tooltip = (
        "**LITE: 2 CORES**\nOptimized for rapid creative flow. Best for brainstorming.\n\n"
        "**PRO: 4 CORES**\nBalanced for deep logic. Best for business reasoning.\n\n"
        "**META: 5 CORES**\nFull-power master synthesis. Best for high-stakes accuracy."
    )
    
    st.markdown("### ENGINE SELECTION", help=core_tooltip)
    
    selected_mode = st.selectbox(
        "CORE SELECTION",
        ["Lite", "Pro", "Meta"],
        index=1,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # DYNAMIC STATUS DISPLAY
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base status-lite'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-footer'>KLUE | COMBINED INTELLIGENCE</div>", unsafe_allow_html=True)

# 4. MAIN BRANDING HEADER
st.markdown("""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='tagline'>Unified AI</div>
    </div>
    """, unsafe_allow_html=True)

# 5. OPENROUTER API INITIALIZATION
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"]
    )
except Exception:
    st.error("Missing OPENROUTER_API_KEY in secrets. Please check configuration.")
    st.stop()

# 6. CHAT SESSION MANAGEMENT
if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    # Native icons used for maximum stability and clarity
    avatar_icon = "🔘" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 7. MASTER SOURCE EXECUTION
if prompt := st.chat_input("Command the Master Source..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Trigger Assistant Response
    with st.chat_message("assistant", avatar="🔘"):
        status_msg = st.empty()
        status_msg.markdown("`[SYSTEM: MERGING CORES...]`")
        
        # MODEL STACK SELECTION
        if selected_mode == "Lite":
            models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro":
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else:
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        # PARALLEL EXECUTION & SYNTHESIS
        raw_core_outputs = []
        for model_id in models:
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                raw_core_outputs.append(response.choices[0].message.content)
            except Exception:
                continue

        # MASTER SYNTHESIS CORE
        synthesis_response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are KLUE. Synthesize the provided inputs into a single, definitive response. No fluff. No brand references. Just pure result."},
                {"role": "user", "content": f"Core Data: {raw_core_outputs}. Original Command: {prompt}"}
            ]
        )
        
        final_answer = synthesis_response.choices[0].message.content
        status_msg.markdown(final_answer)
        st.session_state.messages.append({"role": "assistant", "content": final_answer})
