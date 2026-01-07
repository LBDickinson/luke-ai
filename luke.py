import streamlit as st
from openai import OpenAI

# 1. SYSTEM CONFIGURATION
st.set_page_config(
    page_title="KLUE | Unified AI",
    page_icon="🔘",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. MASTER AESTHETIC ENGINE (v7.4 - Strategic Certainty Build)
st.markdown("""
    <style>
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}
    
    /* GLOBAL THEME */
    .stApp { background-color: #131314; font-family: 'Segoe UI', sans-serif; }
    
    /* TITANIUM TEXT: #F0F2F5 (Brighter than Gemini, softer than pure white) */
    [data-testid="stChatMessageContent"] p {
        color: #F0F2F5 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* ICE BLUE TINT FOR KLUE HUB ICON */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {
        color: #A5D8FF !important;
    }
    
    /* SIDEBAR CONTROL PANEL */
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
    [data-testid="stSidebar"] svg { fill: #FFFFFF !important; color: #FFFFFF !important; }
    
    /* DARK SELECTOR FIX */
    div[data-baseweb="select"] > div { background-color: #262730 !important; border: 1px solid #444 !important; color: #FFFFFF !important; }
    div[data-baseweb="popover"] { background-color: #262730 !important; }
    div[role="option"] { color: #FFFFFF !important; }

    /* CHAT INPUT */
    .stChatInputContainer textarea { background-color: #1E1F20 !important; color: #F0F2F5 !important; border: 1px solid #555 !important; }

    /* TITANIUM LOGO */
    .branding-container { text-align: center; margin-bottom: 50px; padding-top: 20px; }
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
        padding: 15px 35px; 
        background: linear-gradient(135deg, #8E9EAB 0%, #FFFFFF 50%, #8E9EAB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        border: 2px solid #555; border-bottom-left-radius: 45px; 
        animation: logo-shine 8s linear infinite;
    }
    @keyframes logo-shine { to { background-position: 200% center; } }
    .tagline { color: #FFFFFF !important; font-size: 0.8rem; letter-spacing: 10px; margin-top: 25px; text-transform: uppercase; font-weight: 400; opacity: 0.9; }

    /* CORE STATUS BOXES */
    .status-base { color: #A5D8FF !important; border: 1px solid #A5D8FF !important; padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; text-align: center; letter-spacing: 2px; margin-top: 15px; }
    .status-pro { box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4); border: 2px solid #A5D8FF !important; }
    .status-meta { border: 2px solid #FFFFFF !important; box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6); }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: MISSION & ENGINE SELECTION
with st.sidebar:
    st.markdown("### WHY KLUE?")
    with st.expander("THE CERTAINTY MANIFESTO", expanded=False):
        st.write("""
        **Move with Certainty.** In an era where AI risks mistakes, KLUE is the Audit Layer.
        
        **The Ensemble Architecture:** KLUE engages five world-leading AI engines simultaneously to cross-verify every claim.
        
        **The Firewall:** The probability of 5 architectures telling the same lie is **astronomically low**.
        
        Instead of an answer, you get **THE answer**.
        """)

    st.markdown("---")
    
    core_help = (
        "**LITE: 2 CORES**\nRapid creative flow.\n\n"
        "**PRO: 4 CORES**\nVerified business reasoning.\n\n"
        "**META: 5 CORES**\nMaster oversight & total certainty."
    )
    st.markdown("### ENGINE SELECTION", help=core_help)
    selected_mode = st.selectbox("CORE", ["Lite", "Pro", "Meta"], index=1, label_visibility="collapsed")
    
    if selected_mode == "Lite": st.markdown("<div class='status-base'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)

# 4. BRANDING
st.markdown("<div class='branding-container'><div class='logo'>KLUE</div><div class='tagline'>Unified AI</div></div>", unsafe_allow_html=True)

# 5. OPENROUTER CLIENT
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("Missing OPENROUTER_API_KEY.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []

# 6. CHAT DISPLAY
for msg in st.session_state.messages:
    icon = ":material/hub:" if msg["role"] == "assistant" else ":material/radio_button_checked:"
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# 7. MASTER EXECUTION
if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/radio_button_checked:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=":material/hub:"):
        status = st.empty()
        status.markdown("`[SYSTEM: CONVENING BOARD MEETING...]`")
        
        # Select Models
        if selected_mode == "Lite": cores = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro": cores = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else: cores = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        # Run Cores
        core_data = []
        for c in cores:
            try:
                res = client.chat.completions.create(model=c, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                core_data.append(res.choices[0].message.content)
            except: continue

        # Synthesis
        master = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are KLUE. Provide THE answer. Synthesize core consensus. Dramatically reduce risk. Move with certainty."},
                {"role": "user", "content": f"Cores: {core_data}. Query: {prompt}"}
            ]
        )
        
        final_answer = master.choices[0].message.content
        status.markdown(final_answer)
        st.session_state.messages.append({"role": "assistant", "content": final_answer})
