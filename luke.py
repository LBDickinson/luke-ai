import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Industrial UI (The "No-Nonsense" Look)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    .logo {
        font-family: monospace;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: 10px;
        text-align: center;
        margin-top: -50px;
    }
    
    .tagline {
        text-align: center;
        color: #555;
        font-family: monospace;
        font-size: 0.7rem;
        letter-spacing: 5px;
        margin-bottom: 50px;
    }

    .stChatMessage {
        background-color: #000000;
        border: 1px solid #222;
        border-radius: 0px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("### ENGINE")
    ultra_mode = st.toggle("ULTRA-REASONING", value=False)
    st.caption("v2.1 / CORE-ACTIVE")

st.markdown("<div class='logo'>KLUE</div>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>UNIFIED MULTI-MODEL SYSTEM</div>", unsafe_allow_html=True)

# 4. API
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
except Exception:
    st.error("API Error.")
    st.stop()

# 5. History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Execution
if prompt := st.chat_input("Enter query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if ultra_mode:
            message_placeholder.markdown("`[STATUS: SYNCING ULTRA-REASONING MODELS]`")
            models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]
        else:
            message_placeholder.markdown("`[STATUS: UNIFYING DATA]`")
            models = ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct", "mistralai/mistral-7b-instruct"]
        
        data_stream = []
        for m in models:
            try:
                res = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], max_tokens=500)
                data_stream.append(res.choices[0].message.content)
            except:
                pass

        # Clean Synthesis
        synthesis = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": "You are KLUE. Provide a unified, concise, and factual summary of the data provided. No fluff. No metaphors."},
                {"role": "user", "content": f"Data: {data_stream}. Query: {prompt}"}
            ]
        )

        output = synthesis.choices[0].message.content
        message_placeholder.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})

st.markdown("---")
st.caption("© 2026 L.B. Dickinson | v2.1-Core")
