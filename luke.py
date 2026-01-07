import streamlit as st
from openai import OpenAI

# 1. System Config
st.set_page_config(page_title="KLUE", page_icon="🔘", layout="centered")

# 2. Brushed Metal UI + High-Contrast Typography
st.markdown("""
    <style>
    /* Carbon Black background for depth */
    .stApp { 
        background-color: #080808; 
        color: #D1D1D1; 
    }
    
    /* Ensure all main text is bright white and legible */
    .stMarkdown p, .stMarkdown li, .stMarkdown div {
        color: #E0E0E0 !important;
    }

    .branding-container {
        text-align: center;
        margin-top: -60px;
        margin-bottom: 45px;
    }

    /* Brushed Titanium Logo Style */
    .logo {
        font-family: 'Inter', sans-serif;
        font-size: 4.2rem;
        font-weight: 900;
        letter-spacing: 15px;
        display: inline-block;
        padding: 10px 30px;
        
        /* Matte Silver / Steel Gradient (Brushed Metal) */
        background: linear-gradient(
            135deg, 
            #757F9A 0%, 
            #D7DDE8 50%, 
            #757F9A 100%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        
        /* Subtle Depth Shadow - No "glow" */
        filter: drop-shadow(2px 3px 2px rgba(0,0,0,0.8));
        
        /* Silver Border Box */
        border: 2px solid #555555;
    }
    
    .tagline {
        color: #666666; 
        font-family: monospace;
        font-size: 0.75rem;
        letter-spacing: 8px;
        margin-top: 20px;
        text-transform: uppercase;
    }

    /* Industrial Chat Bubbles */
    .stChatMessage {
        background-color: #111111;
        border: 1px solid #222222;
        border-radius: 2px;
        margin-bottom: 12px;
    }
    
    /* Force chat response text to pure white */
    [data-testid="stChatMessageContent"] p {
        color: #FFFFFF !important;
        font-size: 1.05rem;
    }

    /* Dark Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222222;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Engine Control (The Switch)
with st.sidebar:
    st.markdown("### ENGINE SYSTEM")
    
    # Toggle Switch: Left = Standard, Right = Ultra
    ultra_mode = st.toggle("ACTIVATE ULTRA MODE", value=False)
    
    if ultra_mode:
        st.success("STATUS: INTEGRATING HEAVYWEIGHTS")
        st.caption("Deep-reasoning active. Expect increased latency.")
    else:
        st.info("STATUS: MERGING STANDARD CORES")
        st.caption("High-speed response mode active.")
    
    st.markdown("---")
    st.caption("KLUE v3.4 / CORE-STABLE")

# 4. Branding Header
st.markdown("""
    <div class='branding-container'>
        <div class='logo'>KLUE</div>
        <div class='tagline'>Integrated Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

# 5. Secure API Connection
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
except Exception:
    st.error("Missing API Credentials in Streamlit Secrets.")
    st.stop()

# 6. Session History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Processing & Execution
if prompt := st.chat_input("Enter query..."):
