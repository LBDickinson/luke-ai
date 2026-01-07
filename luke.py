import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Modern "Big Three" Chat UI
st.markdown("""
    <style>
    /* HIDE STREAMLIT DEFAULTS */
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}

    /* GLOBAL DARK THEME */
    .stApp { 
        background-color: #0B0B0B; 
        color: #ECECEC; 
        font-family: 'SNEEEZE', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* CENTERED CHAT CONTAINER */
    .block-container {
        max-width: 750px;
        padding-top: 2rem !important;
    }

    /* THE LOGO (Refined) */
    .branding-container {
        text-align: center;
        margin-bottom: 40px;
    }
    .logo {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 12px;
        display: inline-block;
        padding: 10px 25px;
        background: linear-gradient(135deg, #C0C0C0 0%, #FFFFFF 50%, #C0C0C0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border: 1px solid #333; /* Thinner, more modern border */
    }
    .tagline {
        color: #666; 
        font-size: 0.7rem;
        letter-spacing: 5px;
        margin-top: 15px;
        text-transform: uppercase;
    }

    /* CHAT BUBBLES (Mimicking Claude/ChatGPT) */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }
    
    /* Subtle line between messages like Gemini */
    [data-testid="stChatMessage"]:not(:last-child) {
        border-bottom: 1px solid #1A1A1A !important;
    }

    /* Typography Polish */
    [data-testid="stChatMessageContent"] p {
        color: #D1D1D1 !important;
        font-size: 1.1rem;
        line-height: 1.7;
    }

    /* FLOATING INPUT STYLING */
    .stChatInputContainer {
        background-color: transparent !important;
    }
    .stChatInputContainer > div {
        background-color: #1A1A1A !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Hidden by default for that clean look)
with st.sidebar:
    st.markdown("### ENGINE CONTROL")
    ultra_mode = st.toggle("ULTRA MODE", value=False)
    st.markdown("---")
    st.caption("KLUE v3.6")

# 4. Header
st.markdown("""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='tagline'>The Unified Source</div>
    </div>
    """, unsafe_allow_html=True)

# 5. API Access
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
except:
    st.error("Connection Error.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history without boxes (cleaner look)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Message KLUE..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if ultra_mode:
            message_placeholder.markdown("`[SYNCING ULTRA MODE]`")
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        else:
            message_placeholder.markdown("`[MERGING CORES]`")
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct", "mistralai/mistral-7b-instruct"]
        
        data_stream = []
        for m in models:
            try:
                res = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                data_stream.append(res.choices[0].message.content)
            except:
                pass

        synthesis = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": "You are KLUE. Provide an integrated, factual summary. Minimalist, professional tone."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )

        final_output = synthesis.choices[0].message.content
        message_placeholder.markdown(final_output)
        st.session_state.messages.append({"role": "assistant", "content": final_output})
