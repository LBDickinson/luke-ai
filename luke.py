import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Master Aesthetic (Polished & Shiny)
st.markdown("""
    <style>
    [data-testid="stDecoration"] {display: none;}
    
    .stApp { 
        background-color: #131314; 
        color: #E3E3E3; 
        font-family: 'Segoe UI', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    
    .block-container { max-width: 800px; padding-top: 2rem !important; }

    /* LOGO: SHINING TITANIUM SHIELD */
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
    .tagline { color: #888888; font-size: 0.8rem; letter-spacing: 10px; margin-top: 25px; text-transform: uppercase; font-weight: 300; }

    /* STATUS BOXES: INCREASING LUSTRE */
    .status-base {
        color: #A5D8FF !important;
        border: 1px solid #A5D8FF !important;
        padding: 12px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 1px;
    }

    /* LITE: Matte Ice Blue */
    .status-lite {
        background-color: rgba(165, 216, 255, 0.05);
        opacity: 0.8;
    }

    /* PRO: Glowing Ice Blue */
    .status-pro {
        background-color: rgba(165, 216, 255, 0.15);
        box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.3);
        border: 2px solid #A5D8FF !important;
    }

    /* META: Ultra-Shine Bloom */
    .status-meta {
        background: linear-gradient(90deg, rgba(165,216,255,0.1) 0%, rgba(165,216,255,0.4) 50%, rgba(165,216,255,0.1) 100%);
        background-size: 200% auto;
        box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6);
        border: 2px solid #FFFFFF !important;
        animation: status-shimmer 3s linear infinite;
    }

    @keyframes status-shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    .stChatInputContainer > div {
        background-color: #1E1F20 !important;
        border: 1px solid #3C4043 !important;
        border-radius: 28px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Hierarchy
with st.sidebar:
    st.markdown("### SYSTEM HIERARCHY")
    
    mode_help = (
        "**Lite:** 2 Engines. Optimized for speed and creative brevity.\n\n"
        "**Pro:** 4 Engines. Merged intelligence with cross-verified logic.\n\n"
        "**Meta:** 5 Engines. Frontier-tier power with Deep Search for 'One-Shot' precision."
    )
    
    selected_mode = st.selectbox(
        "OPERATING MODE",
        ["Lite", "Pro", "Meta"],
        index=1,
        help=mode_help
    )
    
    st.markdown("---")
    
    # Status Indicators with tiered shininess
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base status-lite'>LITE CORE ACTIVE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base status-pro'>PRO: UNIFIED INTELLIGENCE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base status-meta'>META: MASTER SYNTHESIS</div>", unsafe_allow_html=True)
        
    st.caption("KLUE v5.4 / THE MASTER SOURCE")

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
    st.error("API Key Error.")
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

        synthesis = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive synthesis. Master-level precision required."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )
        output = synthesis.choices[0].message.content
        message_placeholder.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
