import streamlit as st

# --- Import feature functions ---
from explain_tab import feature_explain_topic
from summarize_tab import feature_summarize_notes
from quiz_tab import feature_generate_quiz
from flashcard_tab import feature_generate_flashcards

# --- Page Config ---
st.set_page_config(
    page_title="MyBuddy - AI Study Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    :root {
        --bg0: #07111a;
        --bg1: #0d1724;
        --panel: rgba(15, 24, 36, 0.86);
        --panel-strong: rgba(19, 29, 42, 0.95);
        --line: rgba(255, 210, 74, 0.14);
        --text: #f6f8fb;
        --muted: #9aa8bb;
        --accent: #ffd24a;
    }

    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }
    body {
        color: var(--text);
        background:
            linear-gradient(135deg, #0e1a2a 0%, #0a1320 32%, #08111a 60%, #070f17 100%);
    }
    .stApp {
        background:
            linear-gradient(160deg, rgba(255, 210, 74, 0.06) 0%, transparent 26%),
            linear-gradient(20deg, rgba(103, 232, 208, 0.05) 0%, transparent 30%),
            linear-gradient(180deg, rgba(9, 16, 25, 0.98), rgba(6, 11, 18, 1));
    }
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 24% 18%, rgba(255, 220, 140, 0.10), transparent 30%),
            radial-gradient(circle at 74% 22%, rgba(111, 231, 216, 0.08), transparent 28%),
            linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
        background-size: auto, auto, 54px 54px, 54px 54px;
        mask-image: linear-gradient(180deg, rgba(0,0,0,0.72), rgba(0,0,0,0.35) 55%, transparent 90%);
        z-index: 0;
    }
    .main {
        background: transparent;
    }
    .main .block-container {
        position: relative;
        z-index: 1;
        padding-top: 0.8rem;
        max-width: 1240px;
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }
    h1, h2, h3, h4, h5 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.03em;
    }
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        padding: 2.6rem 2rem !important;
        min-height: 300px !important;
        border-radius: 24px !important;
        background: linear-gradient(180deg, rgba(16, 24, 36, 0.92), rgba(10, 16, 25, 0.96)) !important;
        border: 1px solid var(--line) !important;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.38) !important;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #ffe17a, #ffbf2f) !important;
        color: #111827 !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.05rem 1.8rem !important;
        height: auto !important;
        font-size: 1.02rem !important;
        font-weight: 800 !important;
        transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease !important;
        box-shadow: 0 18px 36px rgba(255, 191, 47, 0.24) !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 24px 42px rgba(255, 191, 47, 0.32) !important;
        filter: saturate(1.05) brightness(1.02) !important;
    }
    div[data-testid="column"] {
        padding: 0 0.5rem !important;
    }
    button[kind="secondary"] {
        background: linear-gradient(135deg, rgba(28, 38, 52, 0.96), rgba(16, 24, 36, 0.96)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 16px !important;
        padding: 0.78rem 1.35rem !important;
        transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease !important;
    }
    button[kind="secondary"]:hover {
        border-color: rgba(255, 210, 74, 0.55) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.28) !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Initialize Session State ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# --- Back Button ---
def show_back_button():
    if st.button("← Back to Home", type="secondary", key="back_home"):
        st.session_state.app_mode = "Home"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

# --- Home Page ---
def show_home_page():
    # Header
    st.markdown("""
    <div style="position: relative; text-align: center; padding: 3.4rem 0 2.2rem 0; overflow: hidden;">
        <h1 style="color: #FFF0A8; font-size: clamp(3.1rem, 6vw, 4.8rem); margin-bottom: 0.8rem; font-weight: 700; letter-spacing: -0.05em;">
            📚 MyBuddy
        </h1>
        <p style="font-size: clamp(1.15rem, 2vw, 1.6rem); color: #D7E1EE; margin-top: 0.9rem; font-weight: 400; max-width: 760px; margin-left: auto; margin-right: auto;">
            Transform how you study with AI
        </p>
        <p style="color: #9AA8BB; margin-top: 1.2rem; font-size: 1.02rem; font-style: italic;">
            "Learning is not about working harder, it's about working smarter."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container with buttons - USING st.container()
    with st.container(border=True):
        st.markdown('<h2 style="color: #FFD700; text-align: center; margin-bottom: 2rem; font-size: 2rem;">Choose Your Learning Path</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            if st.button("🎓 Explain Concepts", key="btn_explain", type="primary", use_container_width=True, help="Break down complex topics into crystal-clear understanding. Get explanations tailored to your level—from basics to advanced."):
                st.session_state.app_mode = "Explain a Topic"
                st.rerun()
        
        with col2:
            if st.button("⚡ Summarize Smart", key="btn_summarize", type="primary", use_container_width=True, help="Turn hours of reading into minutes of understanding. Upload PDFs or paste text to get key insights instantly."):
                st.session_state.app_mode = "Summarize Notes"
                st.rerun()
        
        with col3:
            if st.button("🎯 Test Yourself", key="btn_quiz", type="primary", use_container_width=True, help="Practice makes permanent. Get instant feedback, detailed explanations, and track your progress."):
                st.session_state.app_mode = "Generate Quiz"
                st.rerun()
        
        with col4:
            if st.button("🧠 Remember Forever", key="btn_flashcards", type="primary", use_container_width=True, help="Build lasting memory through active recall. Interactive Q&A format boosts retention by 200%."):
                st.session_state.app_mode = "Generate Flashcards"
                st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Stats
    st.markdown('<h3 style="color: #FFD700; text-align: center; margin-bottom: 2.5rem; font-size: 1.8rem;">Why MyBuddy Works</h3>', unsafe_allow_html=True)
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%); border-radius: 15px; border: 2px solid #333333;">
            <h2 style="color: #FFD700; margin: 0; font-size: 2.5rem;">⚡</h2>
            <p style="color: #CCCCCC; margin: 1rem 0 0 0; font-size: 1.1rem;">Lightning Fast</p>
            <p style="color: #888888; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Gemini 2.5 AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%); border-radius: 15px; border: 2px solid #333333;">
            <h2 style="color: #FFD700; margin: 0; font-size: 2.5rem;">🎯</h2>
            <p style="color: #CCCCCC; margin: 1rem 0 0 0; font-size: 1.1rem;">Personalized</p>
            <p style="color: #888888; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Adapts to you</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%); border-radius: 15px; border: 2px solid #333333;">
            <h2 style="color: #FFD700; margin: 0; font-size: 2.5rem;">🎓</h2>
            <p style="color: #CCCCCC; margin: 1rem 0 0 0; font-size: 1.1rem;">Study Anywhere</p>
            <p style="color: #888888; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Mobile friendly</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat4:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%); border-radius: 15px; border: 2px solid #333333;">
            <h2 style="color: #FFD700; margin: 0; font-size: 2.5rem;">🔓</h2>
            <p style="color: #CCCCCC; margin: 1rem 0 0 0; font-size: 1.1rem;">Zero Friction</p>
            <p style="color: #888888; margin: 0.5rem 0 0 0; font-size: 0.9rem;">No login needed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0; color: #666666; border-top: 1px solid #2A2A2A;">
        <p style="font-size: 1.1rem; margin-bottom: 0.8rem; color: #888888;">
            Made with ❤️ for students who want to learn better
        </p>
        <p style="font-size: 0.95rem; color: #555555;">
            Powered by Streamlit & Google Gemini • Version 1.0
        </p>
    </div>
    """, unsafe_allow_html=True)


# --- Main Routing ---
if st.session_state.app_mode == "Home":
    show_home_page()
elif st.session_state.app_mode == "Explain a Topic":
    show_back_button()
    feature_explain_topic()
elif st.session_state.app_mode == "Summarize Notes":
    show_back_button()
    feature_summarize_notes()
elif st.session_state.app_mode == "Generate Quiz":
    show_back_button()
    feature_generate_quiz()
elif st.session_state.app_mode == "Generate Flashcards":
    show_back_button()
    feature_generate_flashcards()
