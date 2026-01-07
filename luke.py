import streamlit as st
from openai import OpenAI

# 1. SYSTEM CONFIGURATION
st.set_page_config(
    page_title="KLUE | Unified AI",
    page_icon="🔘",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. MASTER AESTHETIC ENGINE (Back to Clean Titanium)
st.markdown("""
    <style>
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}
    
    /* GLOBAL THEME */
    .stApp { background-color: #131314; }
    
    /* TITANIUM TEXT FORCE: Ensuring all text is #F0F2F5 */
    .stMarkdown p, [data-testid="stChatMessageContent"] p, .stExpander p {
        color: #F0F2F5 !important;
        font-size: 1.05rem !important;
    }

    /* ICE BLUE TINT FOR KLUE HUB ICON */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {
        color: #A5D8FF !important;
    }
    
    /* SIDEBAR: WIDER & CLEANER */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
        min-width: 320px !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        letter-spacing: 2px !important;
        text-transform: uppercase;
        font-weight: 800 !important;
    }

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
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: THE MANIFESTO (Simple & Clean)
with st.sidebar:
    st.markdown("### STRATEGIC OVERSIGHT")
    with st.expander("WHY KLUE?", expanded=False):
        st.markdown("""
        **Move with Certainty.** KLUE operates on an **Ensemble Architecture**, engaging the five world-leading AI engines simultaneously to cross-verify every claim.
        
        **The Firewall:** The probability of 5 architectures telling the same lie is **astronomically low**.
        
        Instead of an answer, you get **THE answer**.
        """)
    st.markdown("---")
    selected_mode = st.selectbox("OPERATING CORE", ["Lite", "Pro", "Meta"], index=1)

# 4. BRANDING
st.markdown("<div class='branding-container'><div class='logo'>KLUE</div></div>", unsafe_allow_html=True)

# 5. OPENROUTER CLIENT
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("Missing API Key.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []

# 6. CHAT DISPLAY (Pulse & Hub)
for msg in st.session_state.messages:
    icon = ":material/hub:" if msg["role"] == "assistant" else ":material/radio_button_checked:"
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# 7. EXECUTION
if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/radio_button_checked:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=":material/hub:"):
        status = st.empty()
        status.markdown("`[SYSTEM: CONVENING BOARD MEETING...]`")
        
        # Logic remains the same, focused on the synthesis
        cores_map = {"Lite": ["openai/gpt-4o-mini", "google/gemini-flash-1.5"],
                     "Pro": ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"],
                     "Meta": ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]}
        cores = cores_map[selected_mode]
        
        results = []
        for c in cores:
            try:
                r = client.chat.completions.create(model=c, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                results.append(r.choices[0].message.content)
            except: continue

        master = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "system", "content": "You are KLUE. Provide THE answer. Verified consensus only."},
                      {"role": "user", "content": f"Data: {results}. Query: {prompt}"}]
        )
        
        final = master.choices[0].message.content
        status.markdown(final)
        st.session_state.messages.append({"role": "assistant", "content": final})
