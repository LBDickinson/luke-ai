import streamlit as st
from openai import OpenAI

# 1. SYSTEM CONFIGURATION
st.set_page_config(
    page_title="KLUE | Unified AI",
    page_icon="🔘",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. MASTER AESTHETIC ENGINE
st.markdown("""
    <style>
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #131314; font-family: 'Segoe UI', sans-serif; }
    
    /* UNIVERSAL TITANIUM WHITE FORCE */
    .stApp p, .stApp label, .stApp span, [data-testid="stMarkdownContainer"] p, 
    [data-testid="stWidgetLabel"] p {
        color: #F0F2F5 !important;
    }

    /* SELECTBOX VISIBILITY FORCE */
    div[data-baseweb="select"] > div {
        color: #F0F2F5 !important;
        background-color: #262730 !important;
        border: 1px solid #444 !important;
    }

    /* TOOLTIP/HELP TEXT FORCE */
    div[data-testid="stTooltipContent"] p, div[data-testid="stTooltipContent"] span, div[data-testid="stTooltipContent"] * {
        color: #F0F2F5 !important;
    }

    /* MANIFESTO DIALOG CONTRAST */
    [data-testid="stDialog"] p, [data-testid="stDialog"] li, [data-testid="stDialog"] h3, [data-testid="stDialog"] blockquote {
        color: #333333 !important;
    }

    /* ICE BLUE TINT FOR ICONS */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {
        color: #A5D8FF !important;
    }
    [data-testid="stWidgetLabel"] svg, [data-testid="collapsedControl"] svg {
        fill: #A5D8FF !important;
        color: #A5D8FF !important;
    }
    
    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }
    
    /* BUTTON STYLING */
    div.stButton > button {
        background-color: transparent;
        border: 1px solid #444;
        color: #F0F2F5 !important;
        width: 100%;
        text-align: left;
    }
    div.stButton > button:hover {
        background-color: #A5D8FF !important;
        color: #131314 !important;
    }
    
    /* LOGO & TAGLINE */
    .branding-container { text-align: center; margin-bottom: 50px; padding-top: 20px; }
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
        padding: 10px 35px 0px 35px; 
        background: linear-gradient(135deg, #8E9EAB 0%, #FFFFFF 50%, #8E9EAB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        border-top: 2px solid #555; border-left: 2px solid #555; border-right: 2px solid #555;
    }
    .logo-sub {
        color: #F0F2F5; font-size: 0.7rem; letter-spacing: 6px; font-weight: 400;
        margin-top: -5px; text-transform: uppercase;
    }

    /* STATUS BOXES & SIDEBAR TAGLINE */
    .status-base {
        color: #A5D8FF !important; border: 1px solid #A5D8FF !important;
        padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 700;
        text-align: center; letter-spacing: 2px; margin-top: 15px;
    }
    .sidebar-tagline {
        color: #F0F2F5; font-size: 0.65rem; letter-spacing: 3px; font-weight: 400;
        text-align: center; margin-top: 10px; text-transform: uppercase; opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. STATE
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = []

def reset_chat():
    if st.session_state.messages:
        summary = st.session_state.messages[0]["content"][:30] + "..."
        st.session_state.history.append({"title": summary, "chat": st.session_state.messages.copy()})
    st.session_state.messages = []

# 4. MANIFESTO (Full Agreed Copy)
@st.dialog("WHY KLUE?", width="large")
def show_manifesto():
    st.markdown("""
    ### **Stop Guessing. Move with Certainty.**
    In an era where AI is fast, cheap, and **risks mistakes**, KLUE is the Audit Layer for the Modern Enterprise.
    ---
    **1. THE ENSEMBLE ARCHITECTURE**
    **KLUE operates on an Ensemble Architecture, engaging the five world-leading AI engines simultaneously to cross-verify every claim.** Most AI tools are a single voice—one model with its own specific blind spots and biases. KLUE triggers a high-level "Board Meeting" between the world’s most powerful intelligences (OpenAI, Anthropic, Google, Meta, and Mistral) to ensure your data is scrutinized from every angle.
    > **The Result:** You aren't betting your business on a single opinion; you are acting on a verified consensus. Instead of just getting an answer, you get **THE answer.**
    **2. THE HALLUCINATION FIREWALL**
    Single AI models are prone to "Hallucination Patterns"—confident, perfectly phrased fabrications. While one model might misinterpret a fact or risk a mistake, the probability of five independent architectures telling the same highly specific lie is **astronomically low.**
    > **The Result:** This multi-core audit **dramatically reduces** your strategic risk by filtering out algorithmic guesswork to deliver absolute clarity.
    **3. PRECISION OVER SPEED**
    Speed is a commodity; Accuracy is a luxury. Think of standard AI as a **Calculator**—great for routine math and daily tasks. Think of KLUE as the **Auditor**—essential for the 20% of decisions that carry 80% of your business risk. 
    > **The Result:** We don't compete on milliseconds; we compete on the **integrity of the outcome.**
    """)
    if st.button("Close"): st.rerun()

# 5. SIDEBAR
with st.sidebar:
    if st.button("＋ NEW CHAT"):
        reset_chat(); st.rerun()
    st.markdown("---")
    st.markdown("### RECENT")
    if not st.session_state.history:
        st.caption("No recent activity")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            if st.button(item["title"], key=f"hist_{i}"):
                st.session_state.messages = item["chat"]; st.rerun()

    for _ in range(12): st.sidebar.write("") 
    
    st.markdown("---")
    if st.button("📖 WHY KLUE?"): show_manifesto()
    
    core_specs = (
        "**LITE: 2 CORES**\nOptimized for rapid creative flow. Best for brainstorming and quick Q&A.\n\n"
        "**PRO: 4 CORES**\nBalanced for deep logic. Best for verified insights and complex reasoning.\n\n"
        "**META: 5 CORES**\nFull-power master synthesis. Best for high-stakes accuracy and definitive results."
    )
    
    st.markdown("### Engine Selection", help=core_specs)
    selected_mode = st.selectbox("CORE SELECTION", ["Lite", "Pro", "Meta"], index=1, label_visibility="visible")
    
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base' style='box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4); border: 2px solid #A5D8FF !important;'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base' style='border: 2px solid #FFFFFF !important; box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6);'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-tagline'>COMBINED INTELLIGENCE</div>", unsafe_allow_html=True)

# 6. BRANDING
st.markdown("""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='logo-sub'>UNIFIED AI</div>
    </div>
    """, unsafe_allow_html=True)

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])

# 7. DISPLAY
for msg in st.session_state.messages:
    icon = ":material/hub:" if msg["role"] == "assistant" else ":material/radio_button_checked:"
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# 8. RUN
if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/radio_button_checked:"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=":material/hub:"):
        status_area = st.empty(); status_area.markdown("`[SYSTEM: CONVENING BOARD MEETING...]`")
        modes = {"Lite": ["openai/gpt-4o-mini", "google/gemini-flash-1.5"],
                 "Pro": ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"],
                 "Meta": ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]}
        cores = modes[selected_mode]
        core_outputs = []
        for c in cores:
            try:
                res = client.chat.completions.create(model=c, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                core_outputs.append(res.choices[0].message.content)
            except: continue
        master = client.chat.completions.create(model="openai/gpt-4o", 
            messages=[{"role": "system", "content": "Provide THE answer. Verified consensus only."},
                      {"role": "user", "content": f"Data: {core_outputs}. Query: {prompt}"}])
        ans = master.choices[0].message.content
        status_area.markdown(ans); st.session_state.messages.append({"role": "assistant", "content": ans})
