import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. High-Legibility Industrial UI
st.markdown("""
    <style>
    /* Carbon Black background for better text contrast */
    .stApp { 
        background-color: #0A0A0A; 
        color: #E0E0E0; 
    }
    
    /* Force all markdown text to be bright off-white */
    .stMarkdown p, .stMarkdown li, .stMarkdown div {
        color: #E0E0E0 !important;
    }

    .branding-container {
        text-align: center;
        margin-top: -60px;
        margin-bottom: 40px;
    }

    /* Metallic Silver Logo */
    .logo {
        font-family: 'Inter', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        letter-spacing: 15px;
        display: inline-block;
        padding: 15px 40px;
        background: linear-gradient(135deg, #C0C0C0 0%, #FFFFFF 25%, #E5E4E2 50%, #BCC6CC 75%, #C0C0C0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 2px #E5E4E2) drop-shadow(0 0 8px rgba(255,255,255,0.3));
        border: 2px solid #C0C0C0;
    }
    
    .tagline {
        color: #888888;
        font-family: monospace;
        font-size: 0.75rem;
        letter-spacing: 6px;
        margin-top: 20px;
    }

    /* High-Contrast Chat Bubbles */
    .stChatMessage {
        background-color: #111111;
        border: 1px solid #333333;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    
    /* Ensure chat text is specifically bright */
    [data-testid="stChatMessageContent"] p {
        color: #FFFFFF !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222222;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Engine Control
with st.sidebar:
    st.markdown("### SYSTEM ENGINE")
    ultra_mode = st.toggle("ULTRA-REASONING", value=False)
    st.markdown("---")
    st.caption("KLUE v3.1 / 2026")

# 4. Logo Header
st.markdown("""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='tagline'>Unified Multi-Model System</div>
    </div>
    """, unsafe_allow_html=True)

# 5. API Access
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
except Exception:
    st.error("Missing API Credentials.")
    st.stop()

# 6. Session Persistence
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Core Logic & Execution
if prompt := st.chat_input("Enter query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if ultra_mode:
            message_placeholder.markdown("`[STATUS: SYNCING ULTRA-REASONING]`")
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        else:
            message_placeholder.markdown("`[STATUS: UNIFYING DATA SOURCES]`")
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct", "mistralai/mistral-7b-instruct"]
        
        data_stream = []
        for m in models:
            try:
                res = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                data_stream.append(res.choices[0].message.content)
            except:
                pass

        # Synthesis
        synthesis = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a unified, technical, and factual summary. No fluff. Use bright white text formatting."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )

        final_output = synthesis.choices[0].message.content
        message_placeholder.markdown(final_output)
        st.session_state.messages.append({"role": "assistant", "content": final_output})

st.markdown("---")
st.caption("© 2026 L.B. Dickinson | v3.1-High-Contrast")
