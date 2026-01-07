import streamlit as st
from openai import OpenAI

# 1. Page Configuration (This sets the browser tab title and icon)
st.set_page_config(page_title="Luke AI", page_icon="⚖️", layout="centered")

# 2. Custom Styling to make it look professional
st.markdown("""
    <style>
    .stApp { max-width: 800px; margin: 0 auto; }
    .main-title { font-size: 3rem; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #666; margin-bottom: 30px; }
    </style>
    """, unsafe_import_html=True)

st.markdown("<h1 class='main-title'>⚖️ Luke</h1>", unsafe_import_html=True)
st.markdown("<p class='sub-title'>The Supreme Court of AI: Consolidating 5 Expert Models for the Truth.</p>", unsafe_import_html=True)

# 3. Securely Access the API Key from Streamlit Advanced Secrets
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
except Exception:
    st.error("Missing API Key. Please add OPENROUTER_API_KEY to your Streamlit Secrets.")
    st.stop()

# 4. Initialize Chat History (So Luke remembers the conversation)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The Chat Input Logic
if prompt := st.chat_input("Ask the Council..."):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Luke is consulting the council...*")

        # The 5 Experts to query
        experts = [
            "openai/gpt-4o-mini", 
            "anthropic/claude-3-haiku", 
            "google/gemini-flash-1.5",
            "meta-llama/llama-3.1-8b-instruct",
            "mistralai/mistral-7b-instruct"
        ]
        
        expert_responses = []

        # The Fan-Out: Querying all 5
        for model_id in experts:
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                expert_responses.append(f"Expert ({model_id}): {response.choices[0].message.content}")
            except Exception as e:
                expert_responses.append(f"Expert ({model_id}) was unavailable for this session.")

        # 6. The Final Synthesis (The Judge Logic)
        judge_system_prompt = """
        You are Luke, a high-level AI auditor. You have been given responses from 5 different AI experts.
        Your goal:
        1. Compare all 5 responses.
        2. Identify the common truth and resolve any contradictions.
        3. If one model is clearly wrong (hallucinating), ignore it.
        4. Provide one concise, authoritative final answer.
        5. Do not mention individual models by name in your final output; speak as the unified voice of Luke.
        """

        final_judgment = client.chat.completions.create(
            model="openai/gpt-4o", # Using the highest quality model for the final judgment
            messages=[
                {"role": "system", "content": judge_system_prompt},
                {"role": "user", "content": f"Here are the expert opinions: {expert_responses}. Now, provide the final answer to the user's original question: {prompt}"}
            ]
        )

        full_response = final_judgment.choices[0].message.content
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# 7. Professional Footer
st.markdown("---")
st.caption("© 2026 L.B. Dickinson | [Terms of Service](https://github.com/LBDickinson/luke-ai/blob/main/TERMS.md)")
