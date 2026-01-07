import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="Luke AI", page_icon="⚖️", layout="centered")

# 2. Custom Styling
st.markdown("""
    <style>
    .stApp { max-width: 800px; margin: 0 auto; }
    .main-title { font-size: 3rem; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #666; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>⚖️ Luke</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>The Supreme Court of AI: Consolidating 5 Expert Models for the Truth.</p>", unsafe_allow_html=True)

# 3. Securely Access API Key
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
except Exception:
    st.error("Missing API Key. Please add OPENROUTER_API_KEY to your Streamlit Secrets.")
    st.stop()

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The Chat Logic
if prompt := st.chat_input("Ask the Council..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Luke is consulting the council...*")

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

        # 6. The Final Judgment
        judge_system_prompt = "You are Luke, a high-level AI auditor. Compare the 5 responses provided, resolve contradictions, and give one concise, authoritative final answer. Do not mention individual models by name."

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
