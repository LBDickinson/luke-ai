import streamlit as st
from openai import OpenAI
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

# 1. SYSTEM CONFIGURATION
st.set_page_config(
    page_title="KLUE | Unified AI",
    page_icon="🔘",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. MASTER AESTHETIC (v7.6 - The "Sleek & Pro" Build)
st.markdown("""
    <style>
    /* 1. HIDE DECORATION & FOOTER */
    [data-testid="stDecoration"] {display: none;}
    footer {visibility: hidden;}
    
    /* 2. GLOBAL DARK THEME & TEXT FORCE */
    .stApp { background-color: #131314; }
    
    /* FORCE TITANIUM WHITE ON ALL UI ELEMENTS */
    [data-testid="stSidebar"], [data-testid="stDialog"], [data-testid="stMarkdownContainer"] p {
        color: #F0F2F5 !important;
    }
    
    /* 3. SIDEBAR WIDTH & STYLE */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #333333;
        min-width: 350px !important;
    }
    
    /* 4. CHAT TEXT TITANIUM WHITE */
    [data-testid="stChatMessageContent"] p {
        color: #F0F2F5 !important;
        font-size: 1.05rem;
    }

    /* 5. ICE BLUE HUB ICON */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {
        color: #A5D8FF !important;
    }

    /* 6. LOGO & BRANDING */
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

# 3. MODAL DIALOG: THE MANIFESTO
@st.dialog("THE CERTAINTY MANIFESTO", width="large")
def show_manifesto():
    st.markdown("""
    ### **Move with Certainty.** In an era where AI risks mistakes, **KLUE is the Audit Layer** for the Modern Enterprise.
    
    **1. THE ENSEMBLE ARCHITECTURE**
    KLUE engages five world-leading AI engines simultaneously to cross-verify every claim. Most AI tools are a single voice; KLUE is a verified consensus.
    
    **2. THE HALLUCINATION FIREWALL**
    While a single model might risk a mistake, the probability of five independent architectures telling the same lie is **astronomically low**.
    
    **3. THE RESULT**
    Instead of just getting an answer, you get **THE answer**. We dramatically reduce strategic risk so you can finally move with total certainty.
    """)
    if st.button("Close"): st.rerun()

# 4. PDF ENGINE
def create_pdf(text):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    c.setFont("Helvetica-Bold", 16); c.drawString(50, 750, "KLUE | UNIFIED INTELLIGENCE REPORT")
    c.line(50, 740, 550, 740)
    c.setFont("Helvetica", 11)
    text_object = c.beginText(50, 710)
    for line in text.split('\n'): text_object.textLine(line)
    c.drawText(text_object); c.showPage(); c.save()
    return buf.getvalue()

# 5. SIDEBAR
with st.sidebar:
    st.markdown("### STRATEGIC OVERSIGHT")
    if st.button("📖 WHY KLUE?"):
        show_manifesto()
    st.markdown("---")
    selected_mode = st.selectbox("OPERATING CORE", ["Lite", "Pro", "Meta"], index=1)
    st.markdown("<br>", unsafe_allow_html=True)
    if selected_mode == "Lite": st.markdown("<div style='border: 1px solid #A5D8FF; padding: 10px; border-radius: 8px; text-align: center; color: #A5D8FF;'>LITE: 2 CORES</div>", unsafe_allow_html=True)
    elif selected_mode == "Pro": st.markdown("<div style='border: 2px solid #A5D8FF; box-shadow: 0 0 10px #A5D8FF; padding: 10px; border-radius: 8px; text-align: center; color: #A5D8FF;'>PRO: 4 CORES</div>", unsafe_allow_html=True)
    else: st.markdown("<div style='border: 2px solid #FFF; box-shadow: 0 0 15px #FFF; padding: 10px; border-radius: 8px; text-align: center; color: #FFF;'>META: 5 CORES</div>", unsafe_allow_html=True)

# 6. MAIN BRANDING
st.markdown("<div class='branding-container'><div class='logo'>KLUE</div></div>", unsafe_allow_html=True)

# 7. EXECUTION
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])
except:
    st.error("API Key Missing."); st.stop()

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    icon = ":material/hub:" if msg["role"] == "assistant" else ":material/radio_button_checked:"
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

if prompt := st.chat_input("Command the Master Source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/radio_button_checked:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=":material/hub:"):
        status = st.empty(); progress = st.progress(0)
        status.markdown("`[SYSTEM: CONVENING BOARD MEETING...]`")
        
        cores_map = {"Lite": ["openai/gpt-4o-mini", "google/gemini-flash-1.5"],
                     "Pro": ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct"],
                     "Meta": ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3.1-405b", "mistralai/mistral-large"]}
        cores = cores_map[selected_mode]
        
        results = []
        for i, c in enumerate(cores):
            try:
                r = client.chat.completions.create(model=c, messages=[{"role": "user", "content": prompt}], max_tokens=600)
                results.append(r.choices[0].message.content)
                progress.progress((i + 1) / (len(cores) + 1))
            except: continue

        master = client.chat.completions.create(model="openai/gpt-4o", 
            messages=[{"role": "system", "content": "You are KLUE. Provide THE answer. Synthesize consensus."},
                      {"role": "user", "content": f"Data: {results}. Query: {prompt}"}])
        
        final = master.choices[0].message.content
        progress.empty(); status.markdown(final)
        st.session_state.messages.append({"role": "assistant", "content": final})
        
        pdf = create_pdf(final)
        st.download_button(label="📥 DOWNLOAD CERTAINTY REPORT", data=pdf, file_name="KLUE_Report.pdf", mime="application/pdf")
