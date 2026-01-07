import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Gemini-Inspired UI (Charcoal & Seamless Sidebar)
st.markdown("""
    <style>
    /* HIDE DEFAULTS */
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}

    /* GLOBAL THEME - Using Gemini's #131314 Charcoal */
    .stApp { 
        background-color: #131314; 
        color: #E3E3E3; 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* SEAMLESS SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important; /* Slightly lighter charcoal for sidebar depth */
        border-right: 1px solid #333333;
    }
    
    /* REMOVE SIDEBAR WHITE TEXT/FOOTER */
    [data-testid="stSidebar"] section {
        background-color: transparent !important;
    }

    /* CENTERED CHAT COLUMN */
    .block-container {
        max-width: 800px;
        padding-top: 2rem !important;
    }

    /* LOGO (Metallic Titanium) */
    .branding-container { text-align: center; margin-bottom: 50px; }
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
        padding: 12px 30px; background: linear-gradient(135deg, #A1A1A1 0%, #FFFFFF 50%, #A1A1A1 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; border: 1px solid #444;
    }
    .tagline { color: #888; font-size: 0.75rem; letter-spacing: 6px; margin-top: 15px; text-transform: uppercase; }

    /* GEMINI-STYLE MESSAGES */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1.5rem 0 !important;
    }
    [data-testid="stChatMessageContent"] p {
        color: #E3E3E3 !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* SEAMLESS BOTTOM INPUT AREA */
    .stChatInputContainer {
        padding-bottom: 2rem !important;
        background-color: #131314 !important;
    }
    .stChatInputContainer > div {
        background-color: #1E1F20 !important;
        border: 1px solid #3C4043 !important;
        border-radius: 28px !important; /* Gemini's rounded input pill */
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Engine Configuration
with st.sidebar:
    st.markdown("### SYSTEM CONFIG")
    
    mode_help = (
        "**Standard:** 2 High-speed engines. Best for simple creative tasks.\n\n"
        "**Balanced:** 4 Engines. Optimized for professional research.\n\n"
        "**Executive:** 5 Heavyweight engines. Provides a high-accuracy 'One-Shot' response, "
        "saving you time on fact-checking and follow-up corrections."
    )
    
    selected_mode = st.selectbox(
        "OPERATING MODE",
        ["Standard", "Balanced", "Executive"],
        index=1,
        help=mode_help
    )
    
    st.markdown("---")
    if selected_mode == "Standard": st.info("HIGH-SPEED CORE")
    elif selected_mode == "Balanced": st.success("UNIFIED LOGIC")
    else: st.warning("EXECUTIVE SYNTHESIS")
    st.caption("KLUE v3.9 / THE UNIFIED SOURCE")

# 4. Branding
st.markdown("""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='tagline'>The Unified Source</div>
    </div>
    """, unsafe_allow_html=True)

# 5. API Logic
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("API Error.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Ask KLUE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if selected_mode == "Standard":
            message_placeholder.markdown("`[STATUS: RUNNING FAST CORES]`")
            models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]
        elif selected_mode == "Balanced":
            message_placeholder.markdown("`[STATUS: MERGING DATA SOURCES]`")
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"]
        else:
            message_placeholder.markdown("`[STATUS: PERFORMING EXECUTIVE SYNTHESIS]`")
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        
        data_stream = []
        for m in models:
            try:
                res = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                data_stream.append(res.choices[0].message.content)
            except: pass

        # Final Merged Output
        synthesis = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a unified, professional response. No fluff."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )

        output = synthesis.choices[0].message.content
        message_placeholder.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
