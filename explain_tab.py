import streamlit as st
import re
from utils import generate_content_with_backoff


# --- CUSTOM CSS FOR EXPLAIN TOPIC ---
def inject_explain_css():
    """Injects custom CSS for explain topic styling"""
    st.markdown("""
    <style>
    /* Primary buttons - Yellow with dark text */
    button[kind="primary"] {
        background-color: #FFD700 !important;
        color: #1A1A1A !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #FFC700 !important;
        color: #1A1A1A !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* Secondary buttons - Gray with gray border, yellow on hover */
    button[kind="secondary"] {
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="secondary"]:hover {
        border-color: #FFD700 !important;
        color: #FFFFFF !important;
        transform: scale(1.02) !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Download button styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        border-color: #FFD700 !important;
        transform: scale(1.02) !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Style bordered containers */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%) !important;
        border-radius: 20px !important;
        border: 2px solid #333333 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        padding: 2.5rem !important;
    }
    
    /* Inline code styling */
    .explanation-content code {
        background-color: #2A2A2A !important;
        color: #FFD700 !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        font-family: 'Courier New', Consolas, Monaco, monospace !important;
        font-size: 0.9em !important;
    }
    
    /* Code block styling */
    .explanation-content pre {
        background-color: #0D1117 !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 0.8rem 0 !important;
        overflow-x: auto !important;
        font-family: 'Courier New', Consolas, Monaco, monospace !important;
        color: #C9D1D9 !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        white-space: pre !important;
    }
    
    /* Bold text styling */
    .explanation-content strong {
        color: #FFD700 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def feature_explain_topic():
    """Implements the 'Explain a Topic' feature with modern UI."""
    
    inject_explain_css()
    
    # Custom header
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2rem;">📚 Explain a Topic</h1>
        <p style="color: #CCCCCC; margin-top: 0.5rem; font-size: 1.1rem;">Get structured, level-appropriate explanations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize state variables
    if 'explanation_output' not in st.session_state:
        st.session_state.explanation_output = None
    if 'explanation_topic' not in st.session_state:
        st.session_state.explanation_topic = ""
    if 'explanation_level' not in st.session_state:
        st.session_state.explanation_level = "Intermediate"
    if 'explanation_generating' not in st.session_state:
        st.session_state.explanation_generating = False
    
    # If showing results, display them
    if st.session_state.explanation_output:
        display_explanation_results()
        return
    
    # Loading state
    if st.session_state.explanation_generating:
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 2rem 1rem; text-align: center;">
                <div style="margin-bottom: 2rem;">
                    <div style="
                        border: 4px solid #333333;
                        border-top: 4px solid #FFD700;
                        border-radius: 50%;
                        width: 60px;
                        height: 60px;
                        animation: spin 1s linear infinite;
                        margin: 0 auto;
                    "></div>
                </div>
                <h3 style="color: #FFD700; margin: 0;">🔄 Generating Explanation...</h3>
                <p style="color: #CCCCCC; margin-top: 0.5rem;">Please wait while we prepare your explanation</p>
            </div>
            
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Actually generate
        generate_explanation()
        return
    
    # Input form
    with st.container(border=True):
        st.markdown('<h3 style="color: #FFD700; margin-top: 0; margin-bottom: 1rem; font-size: 1.3rem;">🎓 What would you like to learn?</h3>', unsafe_allow_html=True)
        
        # Topic input
        topic = st.text_area(
            "Enter your topic or query:", 
            value=st.session_state.explanation_topic,
            height=120,
            placeholder="e.g., The principles of quantum entanglement, How does photosynthesis work?",
            help="Enter any topic you'd like explained"
        )
        
        # Update session state
        if topic != st.session_state.explanation_topic:
            st.session_state.explanation_topic = topic
        
        st.markdown('<div style="margin-top: 1rem;"><h4 style="color: #FFD700; margin: 0 0 0.5rem 0; font-size: 1.05rem;">⚙️ Explanation Level</h4></div>', unsafe_allow_html=True)
        
        # Level selection - use columns for better control
        col_basic, col_inter, col_adv = st.columns(3)
        
        current_level = st.session_state.explanation_level
        
        with col_basic:
            if st.button("Basic", type="primary" if current_level == "Basic" else "secondary", use_container_width=True, key="level_basic"):
                st.session_state.explanation_level = "Basic"
                st.rerun()
        
        with col_inter:
            if st.button("Intermediate", type="primary" if current_level == "Intermediate" else "secondary", use_container_width=True, key="level_inter"):
                st.session_state.explanation_level = "Intermediate"
                st.rerun()
        
        with col_adv:
            if st.button("Advanced", type="primary" if current_level == "Advanced" else "secondary", use_container_width=True, key="level_adv"):
                st.session_state.explanation_level = "Advanced"
                st.rerun()
        
        st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
        
        # Generate button (centered)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Generate Explanation", type="primary", use_container_width=True, key="gen_explain_btn"):
                if topic.strip():
                    st.session_state.explanation_generating = True
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter a topic first.")
        
        st.markdown('</div>', unsafe_allow_html=True)



def generate_explanation():
    """Actually performs the explanation generation."""
    
    topic = st.session_state.explanation_topic
    level = st.session_state.explanation_level
    
    if not topic.strip():
        st.session_state.explanation_generating = False
        st.rerun()
        return
    
    # Define structured prompt with HTML tags
    system_prompt = f"""
    You are 'MyBuddy', an AI study companion. Your goal is to explain the topic provided by the user in a clear, structured format suitable for a student at the '{level}' level.
    
    Strictly follow the four section markers provided below:
    
    #DEFINITION#
    Provide a clear, concise definition of the topic (2-3 sentences).
    
    #EXPLANATION#
    Explain the topic in detail, breaking down complex ideas into understandable parts.
    - Use <strong>bold</strong> for emphasis on key terms.
    - If you need to show code examples, wrap them in <code>inline code</code> for short snippets or <pre>multi-line code blocks</pre> for longer examples.
    - Use natural paragraphs.
    
    #EXAMPLE#
    Provide a practical example or analogy to illustrate the concept.
    - Use <code> tags for code snippets if needed.
    
    #KEY_POINTS#
    List 3-5 key takeaways using bullet points (use - for bullets).
    """
    
    user_prompt = f"Explain the following topic at the {level} level: {topic}"
    
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.9,
            "topK": 40
        },
        "model": "gemini-2.5-flash-preview-05-20"
    }
    
    # Call API
    response_text = generate_content_with_backoff(payload)
    
    if response_text:
        st.session_state.explanation_output = response_text
    
    st.session_state.explanation_generating = False
    st.rerun()


def display_explanation_results():
    """Displays the generated explanation in structured cards."""
    
    inject_explain_css()
    
    # Custom header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2.5rem; margin-bottom: 0.5rem;">✅ Explanation Complete!</h1>
        <p style="color: #999999; margin: 0; font-size: 1rem;">{st.session_state.explanation_topic}</p>
        <p style="color: #FFD700; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Level: {st.session_state.explanation_level}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse output - FIXED
    try:
        sections = {
            "📖 Definition": st.session_state.explanation_output.split("#EXPLANATION#")[0].replace("#DEFINITION#", "").strip(),
            "💡 Detailed Explanation": st.session_state.explanation_output.split("#EXPLANATION#")[-1].split("#EXAMPLE#")[0].strip(),
            "🌟 Example / Analogy": st.session_state.explanation_output.split("#EXAMPLE#")[-1].split("#KEY_POINTS#")[0].strip(),
            "🎯 Key Takeaways": st.session_state.explanation_output.split("#KEY_POINTS#")[-1].strip()
        }
    except IndexError:
        st.error("❌ Error parsing the response. The explanation may be incomplete.")
        st.code(st.session_state.explanation_output)
        sections = {}
    
    # Display cards with cleaned content
    for header, content in sections.items():
        # Clean content before rendering
        cleaned_content = content
        
        # Remove anchor links like [](http://...)
        cleaned_content = re.sub(r'\[\]\(http[s]?://[^\)]+\)', '', cleaned_content)
        
        # Convert <pre> tags to markdown code blocks
        cleaned_content = re.sub(r'<pre>\s*', '\n```\n', cleaned_content)
        cleaned_content = re.sub(r'\s*</pre>', '\n```\n', cleaned_content)
        
        # Convert <code> tags to inline code markdown
        cleaned_content = re.sub(r'<code>(.*?)</code>', r'`\1`', cleaned_content)
        
        # Convert <strong> tags to markdown bold
        cleaned_content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', cleaned_content)
        
        # Header card
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
            padding: 1.5rem 1.5rem 0.8rem 1.5rem;
            border-radius: 15px 15px 0 0;
            border-left: 5px solid #FFD700;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            margin-bottom: 0;
        ">
            <h3 style="color: #FFD700; margin: 0; font-size: 1.15rem;">
                {header}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Content with bordered container (continuous with header)
        with st.container(border=True):
            st.markdown(cleaned_content)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Explain Another Topic", use_container_width=True, type="secondary"):
            st.session_state.explanation_output = None
            st.session_state.explanation_topic = ""
            st.rerun()
    
    with col2:
        # Download as text
        cleaned_output = st.session_state.explanation_output.replace('#DEFINITION#', 'DEFINITION:\n')
        cleaned_output = cleaned_output.replace('#EXPLANATION#', '\n\nEXPLANATION:\n')
        cleaned_output = cleaned_output.replace('#EXAMPLE#', '\n\nEXAMPLE:\n')
        cleaned_output = cleaned_output.replace('#KEY_POINTS#', '\n\nKEY POINTS:\n')
        
        # Remove HTML tags and anchors from download
        cleaned_output = re.sub(r'\[\]\(http[s]?://[^\)]+\)', '', cleaned_output)
        cleaned_output = re.sub(r'<pre>', '\n', cleaned_output)
        cleaned_output = re.sub(r'</pre>', '\n', cleaned_output)
        cleaned_output = re.sub(r'<code>(.*?)</code>', r'\1', cleaned_output)
        cleaned_output = re.sub(r'<strong>(.*?)</strong>', r'\1', cleaned_output)
        
        separator = '=' * 60
        
        download_text = f"""Topic: {st.session_state.explanation_topic}
Level: {st.session_state.explanation_level}

{separator}

{cleaned_output}
"""
        
        st.download_button(
            label="💾 Download Explanation",
            data=download_text,
            file_name=f"explanation_{st.session_state.explanation_topic.replace(' ', '_')[:30]}.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_explain_btn"
        )

    


