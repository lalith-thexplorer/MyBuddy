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
# --- Custom CSS ---
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    body { background-color: #0E0E0E; color: #FFFFFF; }
    .main { background-color: #0E0E0E; }
    .main .block-container { padding-top: 2rem; max-width: 1200px; }
    
    /* Container styling - increased height */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        padding: 3rem 2rem !important;
        min-height: 300px !important;
    }
    
    /* Primary buttons - evenly spaced */
    button[kind="primary"] {
        background: linear-gradient(135deg, #FFD700, #FFC700) !important;
        color: #1A1A1A !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.2rem 2rem !important;
        height: auto !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.6) !important;
    }
    
    /* Even spacing between columns */
    div[data-testid="column"] {
        padding: 0 0.5rem !important;
    }
    
    /* Secondary buttons */
    button[kind="secondary"] {
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="secondary"]:hover {
        border-color: #FFD700 !important;
        transform: scale(1.03) !important;
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
    <div style="text-align: center; padding: 3rem 0 2rem 0;">
        <h1 style="color: #FFD700; font-size: 4rem; margin-bottom: 1rem; font-weight: 700; letter-spacing: -2px;">
            📚 MyBuddy
        </h1>
        <p style="font-size: 1.6rem; color: #CCCCCC; margin-top: 1rem; font-weight: 300;">
            Transform how you study with AI
        </p>
        <p style="color: #888888; margin-top: 1.5rem; font-size: 1.05rem; font-style: italic;">
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
