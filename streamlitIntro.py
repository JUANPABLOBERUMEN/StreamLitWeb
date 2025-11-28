import streamlit as st
import google.generativeai as genai
import time

# Page configuration
st.set_page_config(
    page_title="✶ Gemini Chat Studio ✶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced sophisticated CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Raleway:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Raleway', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%);
        background-attachment: fixed;
    }
    
    h1 {
        font-family: 'Bebas Neue', sans-serif;
        color: #ff8c00;
        text-align: center;
        font-size: clamp(3rem, 8vw, 5rem);
        margin-bottom: 0.5rem;
        text-shadow: 0 0 50px rgba(255, 140, 0, 0.5);
        animation: elegantGlow 3s ease-in-out infinite alternate;
        font-weight: 400;
        letter-spacing: 0.15em;
    }
    
    @keyframes elegantGlow {
        from { 
            text-shadow: 0 0 30px rgba(255, 140, 0, 0.4),
                         0 0 60px rgba(255, 140, 0, 0.2);
        }
        to { 
            text-shadow: 0 0 50px rgba(255, 140, 0, 0.6),
                         0 0 80px rgba(255, 140, 0, 0.3);
        }
    }
    
    .subtitle {
        font-family: 'Raleway', sans-serif;
        text-align: center;
        color: #999;
        margin-bottom: 3rem;
        font-size: clamp(1.1rem, 3vw, 1.5rem);
        font-weight: 300;
        letter-spacing: 0.35em;
        text-transform: uppercase;
    }
    
    /* API Key container */
    .api-key-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 140, 0, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 0.9rem !important;
        padding: 0.8rem 1.2rem !important;
        transition: all 0.4s ease !important;
        font-family: 'Raleway', sans-serif !important;
    }
    
    .stTextInput input:focus {
        border-color: #ff8c00 !important;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stTextInput input::placeholder {
        color: #666 !important;
        font-style: italic !important;
    }
    
    /* Text areas */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 140, 0, 0.15) !important;
        border-radius: 24px !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem !important;
        padding: 2rem !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Raleway', sans-serif !important;
        line-height: 1.8 !important;
        min-height: 500px !important;
        transform-origin: center !important;
    }
    
    .stTextArea textarea:hover {
        transform: scale(1.02) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 140, 0, 0.3) !important;
        box-shadow: 0 0 40px rgba(255, 140, 0, 0.2),
                    0 10px 50px rgba(0, 0, 0, 0.3) !important;
        z-index: 10 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(255, 140, 0, 0.3) !important;
        box-shadow: 0 0 30px rgba(255, 140, 0, 0.2) !important;
        background: rgba(255, 255, 255, 0.04) !important;
        transform: scale(1) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 140, 0, 0.4) !important;
        font-style: italic !important;
    }
    
    /* Send button */
    .stButton button {
        background: linear-gradient(135deg, #ff8c00 0%, #ff7700 50%, #ff6b00 100%) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 3rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        width: 100% !important;
        box-shadow: 0 6px 25px rgba(255, 140, 0, 0.3) !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        font-family: 'Bebas Neue', sans-serif !important;
        position: relative !important;
        overflow: visible !important;
    }
    
    .stButton button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 12px 40px rgba(255, 140, 0, 0.5) !important;
    }
    
    .stButton button:active {
        transform: translateY(-2px) scale(0.99) !important;
        box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.8),
                    0 0 0 20px rgba(255, 140, 0, 0.4),
                    0 0 0 40px rgba(255, 140, 0, 0.2),
                    0 0 0 60px rgba(255, 140, 0, 0.1) !important;
        animation: buttonPulse 0.6s ease-out !important;
    }
    
    @keyframes buttonPulse {
        0% {
            box-shadow: 0 6px 25px rgba(255, 140, 0, 0.3);
        }
        50% {
            box-shadow: 0 0 0 30px rgba(255, 140, 0, 0),
                        0 0 0 60px rgba(255, 140, 0, 0),
                        0 0 0 90px rgba(255, 140, 0, 0);
        }
        100% {
            box-shadow: 0 6px 25px rgba(255, 140, 0, 0.3);
        }
    }
    
    /* Loading dots */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 500px;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 140, 0, 0.15);
        border-radius: 24px;
        padding: 2rem;
    }
    
    .loading-dots {
        display: flex;
        gap: 1rem;
    }
    
    .loading-dot {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #ff8c00;
        animation: dotPulse 1.5s infinite ease-in-out;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.6);
    }
    
    .loading-dot:nth-child(1) {
        animation-delay: 0s;
    }
    
    .loading-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .loading-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    .loading-dot:nth-child(4) {
        animation-delay: 0.6s;
    }
    
    .loading-dot:nth-child(5) {
        animation-delay: 0.8s;
    }
    
    .loading-dot:nth-child(6) {
        animation-delay: 1s;
    }
    
    @keyframes dotPulse {
        0%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        50% {
            transform: scale(1.3);
            opacity: 1;
        }
    }
    
    /* Column labels */
    .column-label {
        font-family: 'Raleway', sans-serif;
        color: rgba(255, 140, 0, 0.8);
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dynamic gradient background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        transition: opacity 0.3s ease;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
            letter-spacing: 0.25em;
        }
        
        .stTextArea textarea {
            min-height: 300px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'model' not in st.session_state:
    st.session_state.model = None
if 'response' not in st.session_state:
    st.session_state.response = ""
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

# Header
st.markdown("<h1>ASK GEMINI</h1>", unsafe_allow_html=True)

# API Key at top right
col_spacer, col_api = st.columns([4, 1])
with col_api:
    api_key_input = st.text_input(
        "API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="API Key...",
        label_visibility="collapsed"
    )
    
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        if api_key_input:
            try:
                genai.configure(api_key=api_key_input)
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if '-exp' not in m.name.lower():
                            available_models.append(m.name)
                
                if available_models:
                    preferred = [m for m in available_models if 'flash' in m.lower()]
                    st.session_state.model = preferred[0] if preferred else available_models[0]
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("<br>", unsafe_allow_html=True)

# Main layout - Two columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="column-label">ME</div>', unsafe_allow_html=True)
    
    prompt = st.text_area(
        "Prompt",
        height=500,
        placeholder="Escribe tu pregunta aquí...",
        label_visibility="collapsed",
        key="prompt_input"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    send_button = st.button("✦ SEND")

with col2:
    # Dynamic label based on loading state
    label_text = "Gemini is thinking..." if st.session_state.is_loading else "GEMINI"
    st.markdown(f'<div class="column-label">{label_text}</div>', unsafe_allow_html=True)
    
    response_placeholder = st.empty()
    
    if st.session_state.is_loading:
        # Show loading dots
        response_placeholder.markdown("""
        <div class="loading-container">
            <div class="loading-dots">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show response
        response_placeholder.text_area(
            "Response",
            value=st.session_state.response,
            height=500,
            placeholder="La respuesta aparecerá aquí...",
            label_visibility="collapsed",
            disabled=True,
            key="response_output"
        )

# Process message
if send_button:
    if not st.session_state.api_key:
        st.error("⚠ Por favor ingresa tu API Key")
    elif not st.session_state.model:
        st.error("⚠ No se pudo conectar con Gemini API")
    elif not prompt.strip():
        st.error("⚠ Por favor escribe un prompt")
    else:
        st.session_state.is_loading = True
        st.session_state.response = ""
        st.rerun()

# Generate response
if st.session_state.is_loading:
    try:
        model = genai.GenerativeModel(st.session_state.model)
        response = model.generate_content(prompt)
        
        st.session_state.response = response.text
        st.session_state.is_loading = False
        time.sleep(0.5)
        st.rerun()
        
    except Exception as e:
        st.session_state.response = f"❌ Error: {str(e)}"
        st.session_state.is_loading = False
        st.rerun()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 1rem; font-family: \"Raleway\", sans-serif; letter-spacing: 0.1em;'>"
    "Powered by Google Gemini AI • Designer by Berumen in 2025"
    "</p>",
    unsafe_allow_html=True
)