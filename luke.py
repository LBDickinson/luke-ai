import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Master Aesthetic (High Contrast & Tiered Lustre)
st.markdown("""
    <style>
    /* 1. CLEANUP */
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    
    /* 2. GLOBAL THEME (High-Contrast White Text) */
    .stApp { 
        background-color: #131314; 
        color: #FFFFFF !important; 
        font-family: 'Segoe UI', sans-serif;
    }

    /* 3. SIDEBAR VISIBILITY FIX */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    /* Force all sidebar text to be Bright White */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    .block-container { max-width: 800px; padding-top: 2.5rem !important; }

    /* 4. LOGO: SHINING TITANIUM SHIELD */
    .branding-container { text-align: center; margin-bottom: 50px; }
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
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
    .tagline { color: #FFFFFF !important; font-size: 0.8rem; letter-spacing: 10px; margin-top: 25px; text-transform: uppercase; font-weight: 400; opacity: 0.9; }

    /* 5. TIERED ICE BLUE STATUS BOXES */
    .status-base {
        color: #A5D8FF !important;
        border: 1px solid #A5D8FF !important;
        padding: 12px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
        text-align: center;
        letter-spacing: 2px;
        margin-top: 10px;
    }

    /* LITE: Clean Static */
    .status-lite {
        background-color: rgba(165, 216, 255, 0.05);
    }

    /* PRO: Glowing */
    .status-pro {
        background-color: rgba(165, 216, 255, 0.1);
        box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4);
        border: 2px solid #A5D8FF !important;
    }

    /* META: Shimmering Bloom */
    .status-meta {
        background: linear-gradient(90deg, rgba(165,216,255,0.1) 0%, rgba(165,216,255,0.4) 50%, rgba(165,216,255,0.1) 100%);
        background-size: 200% auto;
        box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6);
        border: 2px solid #FFFFFF !important;
        animation: shimmer 4s linear infinite;
    }
    @keyframes shimmer { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }

    /* 6. INPUT PILL STYLING */
    .stChatInputContainer > div {
        background-color: #1E1F20 !important;
        border: 1px solid #555 !important;
        border-radius: 28px !important;
    }
    textarea { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("### SYSTEM HIERARCHY")
    
    mode_help = (
        "**Lite:** 2 Rapid Engines. Speed-optimized for concise tasks.\n\n"
        "**Pro:** 4 Integrated Engines. Deep-reasoning logic for verified results.\n\n"
        "**Meta:** 5 Frontier Engines. Full-power Master Insight for high-stakes accuracy."
    )
    
    selected_mode = st.selectbox(
        "OPERATING MODE",
        ["Lite", "Pro", "Meta"],
        index=1,
        help=mode_help
    )
    
    st.markdown("---")
    
    # Status Indicators
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base status-lite'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)
        
    st.caption("KLUE v5.5 / THE MASTER SOURCE")

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
    st.error("API Secret Missing.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

# 6. Execution
if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Engine Routing
        if selected_mode == "Lite":
            message_placeholder.markdown("`[STATUS: DEPLOYING LITE CORES]`")
            models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro":
            message_placeholder.markdown("`[STATUS: MERGING PRO LOGIC]`")
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else:
            message_placeholder.markdown("`[STATUS: ENGAGING META DEEP SEARCH]`")
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        data_stream = []
        for m in models:
            try:
                res = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                data_stream.append(res.choices[0].message.content)
            except: pass

        # Final Synthesis
        synthesis = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive, no-fluff synthesis. Master-level precision required."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )
        output = synthesis.choices[0].message.content
        message_placeholder.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
