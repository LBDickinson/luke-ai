import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Master Aesthetic (V5.9 Refined)
st.markdown("""
    <style>
    /* BASE THEME */
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    .stApp { background-color: #131314; color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] { background-color: #1E1F20 !important; border-right: 1px solid #333333; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; font-weight: 600 !important; }
    
    /* INPUT BAR LEGIBILITY (White text on dark grey) */
    .stChatInputContainer textarea {
        background-color: #1E1F20 !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
        border-radius: 28px !important;
    }

    /* TITANIUM LOGO ANIMATION */
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
    .status-pro { background-color: rgba(165, 216, 255, 0.1); box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4); border: 2px solid #A5D8FF !important; }
    .status-meta { background: linear-gradient(90deg, rgba(165,216,255,0.1) 0%, rgba(165,216,255,0.4) 50%, rgba(165,216,255,0.1) 100%); background-size: 200% auto; box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6); border: 2px solid #FFFFFF !important; animation: shimmer 4s linear infinite; }
    @keyframes shimmer { 0% { background-position: 0% center; } 100% { background-position: 200% center; } }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Logic Toggles)
with st.sidebar:
    st.markdown("### ENGINE SELECTION", help="LITE: 2 Cores | PRO: 4 Cores | META: 5 Cores")
    selected_mode = st.selectbox("MODE", ["Lite", "Pro", "Meta"], index=1, label_visibility="collapsed")
    st.markdown("---")
    if selected_mode == "Lite": st.markdown("<div class='status-base status-lite'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)

# 4. Main Header
st.markdown("<div class='branding-container'><div class='logo'>KLUE</div><div class='tagline'>Unified AI</div></div>", unsafe_allow_html=True)

# 5. OpenRouter Client
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("Missing OpenRouter Key in Secrets.")
    st.stop()

# 6. Chat Flow
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
        
        # Select Models based on Mode
        if selected_mode == "Lite": models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Pro": models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else: models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        # Collect parallel data
        results = []
        for m in models:
            try:
                res = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=400)
                results.append(res.choices[0].message.content)
            except: pass

        # Master Synthesis Core
        synth = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a definitive, Unified AI synthesis. No fluff."},
                {"role": "user", "content": f"Inputs: {results}. Task: {prompt}"}
            ]
        )
        final_text = synth.choices[0].message.content
        placeholder.markdown(final_text)
        st.session_state.messages.append({"role": "assistant", "content": final_text})
