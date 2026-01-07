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
    
    /* UNIVERSAL TEXT FORCE */
    .stApp p, .stApp label, [data-testid="stMarkdownContainer"] p, .stSelectbox label p {
        color: #F0F2F5 !important;
    }

    /* SELECTOR BOX: FIX WHITE-ON-WHITE */
    /* Target the container background and the text span simultaneously */
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        color: #F0F2F5 !important;
        border: 1px solid #444 !important;
    }
    div[data-baseweb="select"] span {
        color: #F0F2F5 !important;
    }

    /* ARROWS & COLLAPSE CONTROL */
    [data-testid="collapsedControl"] svg {
        fill: #F0F2F5 !important;
        color: #F0F2F5 !important;
    }

    /* SIDEBAR STYLE (Native width restored for manual resize) */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
    }

    /* LOGO BOX - REINFORCED */
    .branding-container { text-align: center; margin-bottom: 50px; padding-top: 20px; }
    .logo {
        font-size: 3.2rem; font-weight: 800; letter-spacing: 12px; display: inline-block;
        padding: 15px 35px 20px 35px; 
        background: linear-gradient(135deg, #8E9EAB 0%, #FFFFFF 50%, #8E9EAB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        border: 2px solid #555 !important;
        border-bottom-left-radius: 45px;
    }
    .logo-sub {
        color: #F0F2F5; font-size: 0.7rem; letter-spacing: 6px; font-weight: 400;
        text-transform: uppercase; margin-top: 10px;
    }

    /* STATUS BOXES */
    .status-base {
        color: #A5D8FF !important; border: 1px solid #A5D8FF !important;
        padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 700;
        text-align: center; letter-spacing: 2px; margin-top: 15px;
    }

    /* HELP ICON */
    [data-testid="stWidgetLabel"] svg {
        fill: #A5D8FF !important;
        color: #A5D8FF !important;
    }
    
    /* BUTTONS */
    div.stButton > button {
        background-color: transparent !important;
        border: 1px solid #444 !important;
        color: #F0F2F5 !important;
    }
    div.stButton > button:hover {
        background-color: #A5D8FF !important;
        color: #131314 !important;
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

# 4. MANIFESTO (Full Copy)
@st.dialog("WHY KLUE?", width="large")
def show_manifesto():
    st.write("### **Stop Guessing. Move with Certainty.**")
    st.write("In an era where AI is fast, cheap, and **risks mistakes**, KLUE is the Audit Layer for the Modern Enterprise.")
    st.write("---")
    st.write("**1. THE ENSEMBLE ARCHITECTURE**")
    st.write("**KLUE operates on an Ensemble Architecture, engaging the five world-leading AI engines simultaneously to cross-verify every claim.** Most AI tools are a single voice—one model with its own specific blind spots and biases. KLUE triggers a high-level 'Board Meeting' between the world’s most powerful intelligences to ensure your data is scrutinized from every angle.")
    st.write("> **The Result:** You aren't betting your business on a single opinion; you are acting on a verified consensus. Instead of just getting an answer, you get **THE answer.**")
    st.write("**2. THE HALLUCINATION FIREWALL**")
    st.write("Single AI models are prone to 'Hallucination Patterns'—confident, perfectly phrased fabrications. While one model might misinterpret a fact, the probability of five independent architectures telling the same highly specific lie is **astronomically low.**")
    st.write("> **The Result:** This multi-core audit **dramatically reduces** your strategic risk by filtering out algorithmic guesswork to deliver absolute clarity.")
    st.write("**3. PRECISION OVER SPEED**")
    st.write("Speed is a commodity; Accuracy is a luxury. Think of standard AI as a **Calculator**—great for routine math. Think of KLUE as the **Auditor**—essential for the 20% of decisions that carry 80% of your business risk.")
    st.write("> **The Result:** We don't compete on milliseconds; we compete on the **integrity of the outcome.**")
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

    # Manual push to bottom
    for _ in range(15): st.sidebar.write("") 
    
    st.markdown("---")
    if st.button("📖 WHY KLUE?"): show_manifesto()
    
    core_specs = (
        "**LITE: 2 CORES**\nOptimized for rapid creative flow. Best for brainstorming and quick Q&A.\n\n"
        "**PRO: 4 CORES**\nBalanced for deep logic. Best for verified insights and complex reasoning.\n\n"
        "**META: 5 CORES**\nFull-power master synthesis. Best for high-stakes accuracy and definitive results."
    )
    
    st.markdown("### Engine Selection", help=core_specs)
    selected_mode = st.selectbox("Engine Selection", ["Lite", "Pro", "Meta"], index=1, label_visibility="collapsed")
    
    if selected_mode == "Lite": 
        st.markdown("<div class='status-base'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": 
        st.markdown("<div class='status-base' style='box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4); border: 2px solid #A5D8FF !important;'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='status-base' style='border: 2px solid #FFFFFF !important; box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6);'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='color:#F0F2F5; font-size:0.65rem; letter-spacing:3px; text-align:center; margin-top:10px; text-transform:uppercase;'>COMBINED INTELLIGENCE</div>", unsafe_allow_html=True)

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
