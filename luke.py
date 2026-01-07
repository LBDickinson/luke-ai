import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Master Aesthetic (V6.2 - The "Final Polish" Build)
st.markdown("""
    <style>
    /* GLOBAL RESET */
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    .stApp { background-color: #131314; color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; }

    /* SIDEBAR: HIGH CONTRAST DARK */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    
    /* SELECTOR FIX: DARK BACKGROUND, WHITE TEXT, NO WHITE-ON-WHITE */
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        border: 1px solid #444 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="popover"] {
        background-color: #262730 !important;
    }
    div[role="option"] {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }
    div[role="option"]:hover {
        background-color: #3D3E47 !important;
        color: #A5D8FF !important;
    }
    
    /* Ensure sidebar labels are visible */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* CHAT INPUT: WHITE ON DARK GREY */
    .stChatInputContainer textarea {
        background-color: #1E1F20 !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
        border-radius: 28px !important;
    }

    /* TITANIUM LOGO */
    .branding-container { text-align: center; margin-bottom: 50px; padding-top: 40px; }
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
    .tagline { color: #FFFFFF !important; font-size: 0.8rem; letter-spacing: 10px; margin-top: 25px; text-transform: uppercase; font-weight: 400; }

    /* CORE STATUS BOXES */
    .status-base { color: #A5D8FF !important; border: 1px solid #A5D8FF !important; padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; text-align: center; letter-spacing: 2px; margin-top: 10px; }
    .status-lite { background-color: rgba(165, 216, 255, 0.05); }
    .status-pro { background-color: rgba(165, 216, 255, 0.1); border: 2px solid #A5D8FF !important; box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4); }
    .status-meta { background: linear-gradient(90deg, rgba(165,216,255,0.1) 0%, rgba(165,216,255,0.4) 50%, rgba(165,216,255,0.1) 100%); background-size: 200% auto; border: 2px solid #FFFFFF !important; box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6); animation: shimmer 4s linear infinite; }
    @keyframes shimmer { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Logic & Tooltips)
with st.sidebar:
    # Restoring the improved core descriptors
    core_help = (
        "**LITE: 2 CORES**\nOptimized for rapid creative flow.\n\n"
        "**PRO: 4 CORES**\nBalanced for deep logic and business reasoning.\n\n"
        "**META: 5 CORES**\nFull-power master synthesis for high-stakes accuracy."
    )
    
    st.markdown("### ENGINE SELECTION", help=core_help)
    selected_mode = st.selectbox("OPERATING MODE", ["Lite", "Pro", "Meta"], index=1, label_visibility="collapsed")
    st.markdown("---")
    
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base status-lite'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)
    
    st.markdown("<br><div style='font-size:0.7rem; letter-spacing:2px; color:grey;'>KLUE | COMBINED INTELLIGENCE</div>", unsafe_allow_html=True)

# 4. Header
st.markdown("<div class='branding-container'><div class='logo'>KLUE</div><div class='tagline'>Unified AI</div></div>", unsafe_allow_html=True)

# 5. OpenRouter Init
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("API Secret Key Missing.")
    st.stop()

# 6. Chat Logic
if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = "🔘" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🔘"):
        placeholder = st.empty()
        placeholder.markdown("`[SYNTESIZING FROM CORES...]`")
        
        # Mode Selection
        if selected_mode == "Lite":
            models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro":
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else:
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        # Core Execution
        results = []
        for m in models:
            try:
                r = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=500)
                results.append(r.choices[0].message.content)
            except: pass

        # Synthesis
        final = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive, Unified AI synthesis. No blah-blah."},
                {"role": "user", "content": f"Core Inputs: {results}. User Query: {prompt}"}
            ]
        )
        ans = final.choices[0].message.content
        placeholder.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
