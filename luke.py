import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Master Aesthetic + Visibility Overrides
st.markdown("""
    <style>
    /* 1. SEAMLESS HEADER & TOGGLE VISIBILITY */
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}

    /* FORCE SIDEBAR ARROW TO BE BRIGHT WHITE & VISIBLE */
    button[data-testid="stBaseButton-headerNoPadding"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        width: 32px;
        height: 32px;
        filter: drop-shadow(0px 0px 3px rgba(255,255,255,0.5));
    }

    /* 2. GLOBAL THEME (Gemini Charcoal) */
    .stApp { 
        background-color: #131314; 
        color: #E3E3E3; 
        font-family: 'Segoe UI', sans-serif;
    }

    /* 3. SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    .block-container { max-width: 800px; padding-top: 2rem !important; }

    /* 4. THE LOGO: ARCHITECTURAL SHIELD */
    .branding-container { text-align: center; margin-bottom: 50px; }
    
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
        padding: 15px 35px; 
        
        /* Shining Titanium Gradient */
        background: linear-gradient(135deg, #8E9EAB 0%, #FFFFFF 50%, #8E9EAB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        
        /* The Shield Box: Architectural Asymmetry */
        border: 2px solid #444;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
        border-bottom-left-radius: 45px; 
        
        /* Depth Shadow */
        filter: drop-shadow(4px 4px 10px rgba(0,0,0,0.6));
        animation: shine 8s linear infinite;
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }

    .tagline { 
        color: #888888; 
        font-size: 0.8rem; 
        letter-spacing: 10px; 
        margin-top: 25px; 
        text-transform: uppercase;
        font-weight: 300;
    }

    /* 5. ICE BLUE STATUS INDICATOR */
    .merged-status {
        color: #A5D8FF;
        border: 1px solid #A5D8FF;
        padding: 12px;
        border-radius: 8px;
        background-color: rgba(165, 216, 255, 0.05);
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 1px;
    }

    /* 6. INPUT PILL STYLING */
    .stChatInputContainer > div {
        background-color: #1E1F20 !important;
        border: 1px solid #3C4043 !important;
        border-radius: 28px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("### SYSTEM HIERARCHY")
    
    mode_help = (
        "**Lite:** 2 Engines. Optimized for creative speed and brevity.\n\n"
        "**Standard:** 4 Engines. Integrated cross-verification and logic merging.\n\n"
        "**Meta:** 5 Engines. The master synthesis for a definitive 'One-Shot' response, "
        "minimizing the need for corrections."
    )
    
    selected_mode = st.selectbox(
        "OPERATING MODE",
        ["Lite", "Standard", "Meta"],
        index=1,
        help=mode_help
    )
    
    st.markdown("---")
    
    if selected_mode == "Lite": 
        st.info("SPEED CORE ACTIVE")
    elif selected_mode == "Standard": 
        st.markdown("<div class='merged-status'>MERGED INTELLIGENCE</div>", unsafe_allow_html=True)
    else: 
        st.warning("META: EXECUTIVE SYNTHESIS")
        
    st.caption("KLUE v4.6 / THE MASTER SOURCE")

# 4. Header
st.markdown(f"""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='tagline'>Unified Ai</div>
    </div>
    """, unsafe_allow_html=True)

# 5. API Logic
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("Credential Error: Check Streamlit Secrets.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

# 6. Core Logic
if prompt := st.chat_input("Query the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if selected_mode == "Lite":
            message_placeholder.markdown("`[STATUS: DEPLOYING SPEED CORES]`")
            models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Standard":
            message_placeholder.markdown("`[STATUS: MERGING UNIFIED LOGIC]`")
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else:
            message_placeholder.markdown("`[STATUS: PERFORMING META SYNTHESIS]`")
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        data_stream = []
        for m in models:
            try:
                res = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                data_stream.append(res.choices[0].message.content)
            except: pass

        # Master Synthesis Output
        synthesis = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive, high-accuracy synthesis. Technical and professional tone only."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )

        output = synthesis.choices[0].message.content
        message_placeholder.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
