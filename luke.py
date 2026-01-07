import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="Luke AI", page_icon="⚖️", layout="centered")

# 2. Premium Branding & Layout
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #1e1e2f 0%, #0e1117 100%);
        color: #f0f2f6;
    }
    .main-title {
        font-family: 'Times New Roman', serif;
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        color: #d4af37;
        margin-top: -30px;
    }
    .sub-title {
        text-align: center;
        color: #a0a0a0;
        font-size: 1rem;
        letter-spacing: 2px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        background-color: rgba(255, 255, 255, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Toggle for Premium Mode
with st.sidebar:
    st.title("Settings")
    is_premium = st.toggle("Supreme Court Mode", value=False)
    if is_premium:
        st.warning("Premium Brains Engaged: Higher accuracy, slower response.")
    else:
        st.info("Standard Mode: High-speed factual consensus.")

st.markdown("<h1 class='main-title'>⚖️ Luke</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Consolidating the World's Best AI Experts</p>", unsafe_allow_html=True)

# 4. Securely Access API Key
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
except Exception:
    st.error("Missing API Key. Please add OPENROUTER_API_KEY to your Streamlit Secrets.")
    st.stop()

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. The Chat Logic
if prompt := st.chat_input("Ask the Council..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Determine which models to use based on the toggle
        if is_premium:
            message_placeholder.markdown("⚖️ **Supreme Court Mode Active...** Deep-analyzing with Heavyweight Experts.")
            experts = [
                "openai/gpt-4o",
                "anthropic/claude-3.5-sonnet",
                "google/gemini-pro-1.5",
                "meta-llama/llama-3.1-405b",
                "mistralai/mistral-large"
            ]
        else:
            message_placeholder.markdown("🔍 **Standard Mode...** Consulting the Council for a quick consensus.")
            experts = [
                "openai/gpt-4o-mini", 
                "anthropic/claude-3-haiku", 
                "google/gemini-flash-1.5",
                "meta-llama/llama-3.1-8b-instruct",
                "mistralai/mistral-7b-instruct"
            ]
        
        expert_responses = []
        for model_id in experts:
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                expert_responses.append(f"Expert ({model_id}): {response.choices[0].message.content}")
            except Exception:
                expert_responses.append(f"Expert ({model_id}) was unavailable.")

        # Final Judgment
        judge_system_prompt = """
        You are Luke, the Supreme AI Auditor. Provide a single, unified response based on the expert data provided.
        1. Combine the best parts of every response into one definitive, factual answer.
        2. Do not mention that you are an AI or that you are 'consulting' models.
        3. Be direct, authoritative, and structured.
        """

        final_judgment = client.chat.completions.create(
            model="openai/gpt-4o", 
            messages=[
                {"role": "system", "content": judge_system_prompt},
                {"role": "user", "content": f"Expert opinions: {expert_responses}. User question: {prompt}"}
            ]
        )

        full_response = final_judgment.choices[0].message.content
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

st.markdown("---")
st.caption("© 2026 L.B. Dickinson | [Terms of Service](https://github.com/LBDickinson/luke-ai/blob/main/TERMS.md)")
