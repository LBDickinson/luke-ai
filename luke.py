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
    
    /* TITANIUM WHITE FORCE (General) */
    [data-testid="stChatMessageContent"] p, .stMarkdown p, label {
        color: #F0F2F5 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* MANIFESTO DIALOG: MAXIMUM CONTRAST CHARCOAL */
    [data-testid="stDialog"] p, [data-testid="stDialog"] li, [data-testid="stDialog"] h3 {
        color: #333333 !important;
        font-weight: 600;
    }

    /* ICE BLUE TINT FOR KLUE HUB ICON */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {
        color: #A5D8FF !important;
    }
    
    /* SIDEBAR: TUNED WIDTH */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
        min-width: 300px !important;
    }
    [data-testid="stSidebar"] h3 { color: #FFFFFF !important; letter-spacing: 2px !important; text-transform: uppercase; font-weight: 800 !important; }

    /* FORCE HELP ICON TO ICE BLUE */
    [data-testid="stWidgetLabel"] svg {
        fill: #A5D8FF !important;
        color: #A5D8FF !important;
    }
    
    /* BUTTON HOVER: WHY KLUE TURNS ICE BLUE */
    div.stButton > button:first-child {
        background-color: transparent;
        border: 1px solid #555;
        color: #F0F2F5;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #A5D8FF !important;
        border-color: #A5D8FF !important;
        color: #131314 !important; /* Dark text on light blue hover */
    }
    
    /* LOGO */
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

    /* STATUS BOXES */
    .status-base {
        color: #A5D8FF !important; border: 1px solid #A5D8FF !important;
        padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 700;
        text-align: center; letter-spacing: 2px; margin-top: 15px;
    }
    .status-pro { box-shadow: 0px 0px 15px rgba(165, 216, 255, 0.4); border: 2px solid #A5D8FF !important; }
    .status-meta { border: 2px solid #FFFFFF !important; box-shadow: 0px 0px 25px rgba(165, 216, 255, 0.6); }
    </style>
    """, unsafe_allow_html=True)

# 3. PRO POP-UP WINDOW (Manifesto)
@st.dialog("WHY KLUE?", width="large")
def show_manifesto():
    st.markdown("""
    ### **Stop Guessing. Move with Certainty.**
    In an era where AI is fast, cheap, and **risks mistakes**, KLUE is the Audit Layer for the Modern Enterprise.
    
    **1. THE ENSEMBLE ARCHITECTURE**
    **KLUE operates on an Ensemble Architecture, engaging the five world-leading AI engines simultaneously to cross-verify every claim.** We trigger a high-level "Board Meeting" between the world’s most powerful intelligences (OpenAI, Anthropic, Google, Meta, and Mistral) to ensure your data is scrutinized from every angle.
    
    *The Result:* You aren't betting your business on a single opinion; you are acting on a verified consensus. Instead of just getting an answer, you get **THE answer.**
    
    **2. THE HALLUCINATION FIREWALL**
    While one model might misinterpret a fact or risk a mistake, the probability of five independent architectures telling the same highly specific lie is **astronomically low.** *The Result:* This multi-core audit **dramatically reduces** your strategic risk by filtering out algorithmic guesswork to deliver absolute clarity.
    
    **3. PRECISION OVER SPEED**
    Think of standard AI as a **Calculator**—great for routine tasks. Think of KLUE as the **Auditor**—essential for the 20% of decisions that carry 80% of your business risk.
    """)
    if st.button("Close"):
        st.rerun()

# 4. SIDEBAR
with st.sidebar:
    st.markdown("### Strategic Oversight")
    if st.button("📖 WHY KLUE?"):
        show_manifesto()
    
    st.markdown("---")
    
    core_specs = (
        "**LITE: 2 CORES**\nOptimized for rapid creative flow. Best for brainstorming and quick Q&A.\n\n"
        "**PRO: 4 CORES**\nBalanced for deep logic. Best for verified insights and complex reasoning.\n\n"
        "**META: 5 CORES**\nFull-power master synthesis. Best for high-stakes accuracy and definitive results."
    )
    
    st.markdown("### Engine Selection", help=core_specs)
    selected_mode = st.selectbox("CORE SELECTION", ["Lite", "Pro", "Meta"], index=1, label_visibility="collapsed")
    
    if selected_mode == "Lite": st.markdown("<div class='status-base'>2 CORES: SPEED RESPONSE</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": st.markdown("<div class='status-base status-pro'>4 CORES: DEEP RESPONSE</div>", unsafe_allow_html=True)
    else: st.markdown("<div class='status-base status-meta'>5 CORES: MASTER INSIGHT</div>", unsafe_allow_html=True)

# 5. BRANDING
st.markdown("<div class='branding-container'><div class='logo'>KLUE</div></div>", unsafe_allow_html=True)

# 6. OPENROUTER CLIENT
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("API Key Missing.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []

# 7. CHAT DISPLAY
for msg in st.session_state.messages:
    icon = ":material/hub:" if msg["role"] == "assistant" else ":material/radio_button_checked:"
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# 8. EXECUTION
if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/radio_button_checked:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=":material/hub:"):
        status_area = st.empty()
        status_area.markdown("`[SYSTEM: MERGING CORES...]`")
        
        cores_map = {"Lite": ["openai/gpt-4o-mini", "google/gemini-flash-1.5"],
                     "Pro": ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"],
                     "Meta": ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]}
        cores = cores_map[selected_mode]
        
        core_outputs = []
        for c in cores:
            try:
                res = client.chat.completions.create(model=c, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                core_outputs.append(res.choices[0].message.content)
            except: continue

        master = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "system", "content": "You are KLUE. Provide a definitive synthesis. Master intelligence mode."},
                      {"role": "user", "content": f"Intelligence Data: {core_outputs}. Command: {prompt}"}]
        )
        
        ans = master.choices[0].message.content
        status_area.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
