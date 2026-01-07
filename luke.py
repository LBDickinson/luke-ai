import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Nuclear CSS - Arrow and Text Visibility
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    footer {visibility: hidden !important;}

    /* THE NUCLEAR ARROW FIX */
    /* Targets the button even when sidebar is collapsed */
    button[kind="headerNoPadding"] svg, 
    .st-emotion-cache-p5msec svg,
    [data-testid="collapsedControl"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        stroke: #FFFFFF !important;
        width: 40px !important;
        height: 40px !important;
        filter: drop-shadow(0px 0px 8px rgba(255,255,255,1)) !important;
        animation: pulse 2s infinite !important;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    /* GLOBAL THEME */
    .stApp { background-color: #131314; color: #FFFFFF !important; }

    /* SIDEBAR TEXT - FORCED WHITE */
    [data-testid="stSidebar"] { background-color: #1E1F20 !important; border-right: 1px solid #333; }
    
    /* Target every text-bearing element in the sidebar */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Specific fix for selectbox text which can be stubborn */
    div[data-baseweb="select"] > div {
        color: #FFFFFF !important;
        background-color: #262730 !important;
    }

    .block-container { max-width: 800px; padding-top: 2rem !important; }

    /* LOGO: SHINING TITANIUM SHIELD */
    .branding-container { text-align: center; margin-bottom: 50px; }
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
        padding: 15px 35px; background: linear-gradient(135deg, #8E9EAB 0%, #FFFFFF 50%, #8E9EAB 100%);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        border: 2px solid #555; border-bottom-left-radius: 45px; 
        filter: drop-shadow(4px 4px 10px rgba(0,0,0,0.6)); animation: shine 8s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .tagline { color: #BBBBBB !important; font-size: 0.85rem; letter-spacing: 10px; margin-top: 25px; text-transform: uppercase; }

    /* ICE BLUE STATUS */
    .unified-status {
        color: #A5D8FF !important; border: 2px solid #A5D8FF !important;
        padding: 12px; border-radius: 8px; background-color: rgba(165, 216, 255, 0.1) !important;
        font-size: 0.85rem; font-weight: 700 !important; text-align: center;
    }

    /* INPUT PILL */
    .stChatInputContainer > div { background-color: #1E1F20 !important; border: 1px solid #555 !important; border-radius: 28px !important; }
    textarea { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("### SYSTEM HIERARCHY")
    mode_help = (
        "**Lite:** 2 Engines. Creative flow.\n\n"
        "**Unified:** 4 Engines. Business logic.\n\n"
        "**Meta:** 5 Engines. Master Deep Search."
    )
    selected_mode = st.selectbox("OPERATING MODE", ["Lite", "Unified", "Meta"], index=1, help=mode_help)
    st.markdown("---")
    if selected_mode == "Lite": st.info("SPEED CORE ACTIVE")
    elif selected_mode == "Unified": st.markdown("<div class='unified-status'>UNIFIED INTELLIGENCE</div>", unsafe_allow_html=True)
    else: st.warning("META: MASTER SYNTHESIS")
    st.caption("KLUE v5.2 / THE MASTER SOURCE")

# 4. Branding
st.markdown(f"""<div class='branding-container'><div class='logo'>KLUE</div><div class='tagline'>Unified Ai</div></div>""", unsafe_allow_html=True)

# 5. API Logic
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("Credential Error.")
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
        elif selected_mode == "Unified":
            message_placeholder.markdown("`[STATUS: MERGING UNIFIED LOGIC]`")
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
                {"role": "system", "content": "You are KLUE. Provide a definitive synthesis. No fluff."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )
        output = synthesis.choices[0].message.content
        message_placeholder.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
