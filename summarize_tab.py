import streamlit as st
import re
from utils import generate_content_with_backoff, extract_text_from_file


# --- CUSTOM CSS FOR SUMMARIZE NOTES ---
def inject_summary_css():
    """Injects custom CSS for summary tab styling"""
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
    
    /* CHECKBOX - Dark gray/black with yellow tick (CSS override) */
    
    /* Unchecked state - dark gray box */
    [data-baseweb="checkbox"] > div:first-child {
        background-color: #2A2A2A !important;
        border: 2px solid #555555 !important;
    }
    
    /* Hover state - yellow border */
    [data-baseweb="checkbox"]:hover > div:first-child {
        border-color: #FFD700 !important;
    }
    
    /* Checked state - dark background with yellow border */
    [data-baseweb="checkbox"] > div:first-child[data-checked="true"] {
        background-color: #1A1A1A !important;
        border: 2px solid #FFD700 !important;
    }
    
    /* Force yellow tick - multiple targeting methods */
    [data-baseweb="checkbox"] svg {
        color: #FFD700 !important;
    }
    
    [data-baseweb="checkbox"] svg path {
        fill: #FFD700 !important;
        stroke: #FFD700 !important;
    }
    
    [data-baseweb="checkbox"] > div:first-child svg {
        color: #FFD700 !important;
    }
    
    [data-baseweb="checkbox"] > div:first-child svg path {
        fill: #FFD700 !important;
        stroke: #FFD700 !important;
    }
    
    /* Nuclear option - override ALL checkbox SVG colors */
    div[data-testid="stCheckbox"] svg {
        color: #FFD700 !important;
    }
    
    div[data-testid="stCheckbox"] svg path {
        fill: #FFD700 !important;
        stroke: #FFD700 !important;
    }
    
    div[data-testid="stCheckbox"] [data-checked="true"] svg {
        color: #FFD700 !important;
    }
    
    div[data-testid="stCheckbox"] [data-checked="true"] svg path {
        fill: #FFD700 !important;
        stroke: #FFD700 !important;
    }
    
    /* Prevent typing in selectbox */
    div[data-baseweb="select"] input {
        pointer-events: none !important;
        cursor: pointer !important;
        caret-color: transparent !important;
        user-select: none !important;
    }
    
    div[data-baseweb="select"] {
        cursor: pointer !important;
    }
    
    /* Style bordered containers */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%) !important;
        border-radius: 20px !important;
        border: 2px solid #333333 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        padding: 2.5rem !important;
    }
    
    /* Reduce spacing in file uploader */
    div[data-testid="stFileUploader"] {
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce spacing in text area */
    div[data-testid="stTextArea"] {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)




def feature_summarize_notes():
    """Implements the 'Summarize Notes' feature with modern UI."""
    
    inject_summary_css()
    
    # Custom header
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2rem;">📝 Summarize Notes</h1>
        <p style="color: #CCCCCC; margin-top: 0.5rem; font-size: 1.1rem;">Condense text or PDF notes for faster learning</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state variables
    if 'summary_output' not in st.session_state:
        st.session_state.summary_output = None
    if 'summary_input_text' not in st.session_state:
        st.session_state.summary_input_text = ""
    if 'summary_length' not in st.session_state:
        st.session_state.summary_length = "Medium"
    if 'summary_style' not in st.session_state:
        st.session_state.summary_style = "Bullet Points"
    if 'summary_generating' not in st.session_state:
        st.session_state.summary_generating = False

    # If showing results, display them
    if st.session_state.summary_output:
        display_summary_results()
        return

    # Loading state
    if st.session_state.summary_generating:
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
                <h3 style="color: #FFD700; margin: 0;">✨ Generating Summary...</h3>
                <p style="color: #CCCCCC; margin-top: 0.5rem;">Please wait while we analyze your notes</p>
            </div>
            
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Actually generate
        generate_summary()
        return

    # Input form
    with st.container(border=True):
        st.markdown('<h3 style="color: #FFD700; margin-top: 0; margin-bottom: 0.8rem; font-size: 1.3rem;">📄 Input Your Notes</h3>', unsafe_allow_html=True)
        
        # File uploader ALWAYS SHOWN (Streamlit handles state automatically)
        uploaded_file = st.file_uploader(
            "Upload PDF or TXT file (max 10MB)", 
            type=["pdf", "txt"],
            help="Upload your notes to summarize. PDFs must be text-based, not scanned images.",
            label_visibility="visible",
            key="file_uploader"
        )
        
        # Store uploaded file in session state
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            # Show indicator that file is active
            st.success(f"✅ File loaded: {uploaded_file.name}")
        elif 'uploaded_file' in st.session_state and st.session_state.uploaded_file:
            # File was uploaded previously
            st.success(f"✅ File loaded: {st.session_state.uploaded_file.name}")
        
        st.markdown('<p style="text-align: center; color: #666666; margin: 0.3rem 0; font-size: 0.9rem;">── OR ──</p>', unsafe_allow_html=True)
        
        # Text area ALWAYS SHOWN
        text_input = st.text_area(
            "Paste your notes here:", 
            value=st.session_state.summary_input_text,
            height=150,
            placeholder="Paste your notes, lecture transcripts, or article text here...",
            help="You can paste text directly instead of uploading a file.",
            key="text_area_input"
        )
        
        # Update session state when text changes
        if text_input != st.session_state.summary_input_text:
            st.session_state.summary_input_text = text_input
            # Clear uploaded file if user starts typing
            if len(text_input.strip()) > 0 and st.session_state.get('uploaded_file'):
                st.session_state.pop('uploaded_file', None)
                st.info("ℹ️ File input cleared - using text input")
        
        # Show which input is active
        has_file = uploaded_file is not None or st.session_state.get('uploaded_file') is not None
        has_text = len(text_input.strip()) > 0
        
        if has_file and has_text:
            st.warning("⚠️ Both file and text detected - text will be used. Clear text to use file.")
        elif has_file:
            st.info("📁 Using file input")
        elif has_text:
            st.info("📝 Using text input")

        
        # Update session state
        if text_input != st.session_state.summary_input_text:
            st.session_state.summary_input_text = text_input
        
        # Store uploaded file in session
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
        
        # Options header with NO anchor link and reduced spacing
        st.markdown('<div style="margin-top: 1rem;"><h4 style="color: #FFD700; margin: 0 0 0.5rem 0; font-size: 1.05rem;">⚙️ Summary Options</h4></div>', unsafe_allow_html=True)
        
        col_style, col_length = st.columns(2)
        
        with col_style:
            summary_style = st.selectbox(
                "Summary Format:",
                ["Bullet Points", "Paragraph", "Both"],
                index=["Bullet Points", "Paragraph", "Both"].index(st.session_state.summary_style),
                help="Choose how you want the summary formatted"
            )
            st.session_state.summary_style = summary_style
            
        with col_length:
            summary_length = st.selectbox(
                "Summary Length:",
                ["Short", "Medium", "Detailed"],
                index=["Short", "Medium", "Detailed"].index(st.session_state.summary_length),
                help="Short: Quick overview | Medium: Balanced | Detailed: Comprehensive"
            )
            st.session_state.summary_length = summary_length
        
        # Toggle button for highlight terms
        current_state = st.session_state.get('highlight_terms', False)
        
        button_label = "🔍 Highlight key terms: " + ("✓ Enabled" if current_state else "Disabled")
        button_style = "primary" if current_state else "secondary"
        
        if st.button(
            button_label,
            key="highlight_toggle",
            type=button_style,
            use_container_width=False
        ):
            st.session_state.highlight_terms = not current_state
            st.rerun()
        
        # Generate button
        st.markdown('<div style="margin-top: 0.8rem;">', unsafe_allow_html=True)
        
        # Generate button with minimal top margin
        st.markdown('<div style="margin-top: 0.8rem;">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Generate Summary", type="primary", use_container_width=True, key="gen_summary_btn"):
                # Validate input - prioritize text over file
                source_text = ""
                
                if text_input.strip():
                    # Text takes priority
                    source_text = text_input
                elif st.session_state.get('uploaded_file') or uploaded_file:
                    # Use file if no text
                    source_text = "file_uploaded"
                
                if not source_text:
                    st.warning("⚠️ Please upload a file or paste text to summarize.")
                elif source_text != "file_uploaded" and len(source_text.strip()) < 50:
                    st.warning("⚠️ Text is too short to summarize. Please provide more content (at least 50 characters).")
                else:
                    st.session_state.summary_generating = True
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)



def generate_summary():
    """Actually performs the summary generation."""
    source_text = ""
    
    # Get text source
    if st.session_state.get('uploaded_file'):
        source_text = extract_text_from_file(st.session_state.uploaded_file)
        if source_text:
            st.session_state.summary_input_text = ""
    elif st.session_state.summary_input_text.strip():
        source_text = st.session_state.summary_input_text
    
    if not source_text or len(source_text.strip()) < 50:
        st.session_state.summary_generating = False
        st.rerun()
        return
    
    # Construct prompt with BETTER highlighting instruction
    highlight_instruction = (
        "Highlight ONLY the 5-7 most critical key terms or concepts using **bold** markdown (e.g., **photosynthesis**). Be selective - do not bold common words or entire phrases, only the most important technical terms or concepts." 
        if st.session_state.get('highlight_terms', False) else 
        "Do not use any bold formatting. Keep all text plain without any markdown."
    )
    
    length_guidance = {
        "Short": "Be very concise. Aim for 3-5 sentences or 3-5 bullet points.",
        "Medium": "Provide a balanced summary. Aim for 1-2 paragraphs or 5-8 bullet points.",
        "Detailed": "Give a comprehensive summary. Aim for 2-3 paragraphs or 8-12 bullet points."
    }
    
    summary_style = st.session_state.summary_style
    summary_length = st.session_state.summary_length
    
    system_prompt = f"""
    You are 'MyBuddy', an AI study companion specialized in creating clear, concise summaries.
    
    Your task:
    - Summarize the provided notes in a {summary_style} format
    - Length: {summary_length} - {length_guidance[summary_length]}
    - Formatting: {highlight_instruction}
    - Focus on the main ideas, key concepts, and important details
    - Use clear, student-friendly language
    - Organize information logically
    
    Important:
    - Do not add information not present in the original text
    - Maintain factual accuracy
    - Be objective and neutral
    """
    
    user_prompt = f"""Summarize the following notes.

Style: {summary_style}
Length: {summary_length}

Notes to summarize:

{source_text}
"""
    
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.3,
            "topP": 0.8,
            "topK": 40
        },
        "model": "gemini-2.5-flash-preview-05-20"
    }
    
    # Call API
    response_text = generate_content_with_backoff(payload)
    
    if response_text:
        st.session_state.summary_output = response_text
        st.session_state.original_text = source_text
    
    st.session_state.summary_generating = False
    st.rerun()


def display_summary_results():
    """Displays the generated summary with stats and actions."""
    
    inject_summary_css()
    
    # Custom header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2.5rem; margin-bottom: 0.5rem;">✅ Summary Complete!</h1>
        <p style="color: #999999; margin: 0; font-size: 1rem;">Your notes have been condensed</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics FIRST
    if st.session_state.get('original_text'):
        original_words = len(st.session_state.original_text.split())
        summary_words = len(st.session_state.summary_output.split())
        reduction = ((original_words - summary_words) / original_words * 100) if original_words > 0 else 0
        
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        
        with col_stats1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border: 2px solid #333333;
                text-align: center;
            ">
                <p style="color: #999999; margin: 0; font-size: 0.9rem; margin-bottom: 0.5rem;">ORIGINAL WORDS</p>
                <p style="color: #FFD700; margin: 0; font-size: 2rem; font-weight: bold;">{original_words}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stats2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border: 2px solid #333333;
                text-align: center;
            ">
                <p style="color: #999999; margin: 0; font-size: 0.9rem; margin-bottom: 0.5rem;">SUMMARY WORDS</p>
                <p style="color: #FFD700; margin: 0; font-size: 2rem; font-weight: bold;">{summary_words}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stats3:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border: 2px solid #333333;
                text-align: center;
            ">
                <p style="color: #999999; margin: 0; font-size: 0.9rem; margin-bottom: 0.5rem;">REDUCTION</p>
                <p style="color: #4CAF50; margin: 0; font-size: 2rem; font-weight: bold;">{reduction:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Summary card SECOND
        # Summary card SECOND with proper formatting (reduced spacing)
    import html
    
    # Process the summary text
    summary_raw = st.session_state.summary_output
    
    # Escape HTML to prevent injection
    summary_escaped = html.escape(summary_raw)
    
    # Handle bold markdown if highlighting is enabled
    if st.session_state.get('highlight_terms', False):
        summary_escaped = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #FFD700;">\1</strong>', summary_escaped)
    
    # Convert markdown bullet points to HTML (REDUCED margin)
    summary_escaped = re.sub(r'^[\-\*]\s+(.+)$', r'<div style="margin-left: 1.5rem; margin-bottom: 0.3rem;">• \1</div>', summary_escaped, flags=re.MULTILINE)
    
    # Convert numbered lists to HTML (REDUCED margin)
    summary_escaped = re.sub(r'^(\d+)\.\s+(.+)$', r'<div style="margin-left: 1.5rem; margin-bottom: 0.3rem;"><strong style="color: #FFD700;">\1.</strong> \2</div>', summary_escaped, flags=re.MULTILINE)
    
    # Convert double line breaks to paragraphs
    summary_escaped = re.sub(r'\n\n', '</p><p style="margin-bottom: 0.8rem;">', summary_escaped)
    
    # Convert single line breaks to <br>
    summary_escaped = summary_escaped.replace('\n', '<br>')
    
    # Wrap in paragraph tags
    summary_html = f'<p style="margin-bottom: 0.8rem;">{summary_escaped}</p>'
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid #333333;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin-bottom: 2rem;
    ">
        <h3 style="color: #FFD700; margin-top: 0; margin-bottom: 1.5rem;">
            📋 {st.session_state.summary_length} Summary ({st.session_state.summary_style})
        </h3>
        <div style="color: #FFFFFF; line-height: 1.8; font-size: 1.05rem;">
            {summary_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    # Action buttons LAST
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Copy Tip", use_container_width=True, type="secondary"):
            st.info("💡 Select the summary text above and use Ctrl+C (Cmd+C on Mac) to copy.")
    
    with col2:
        st.download_button(
            label="💾 Download TXT",
            data=st.session_state.summary_output,
            file_name="mybuddy_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary_btn"
        )
    
    with col3:
        if st.button("🔄 New Summary", use_container_width=True, type="secondary"):
            st.session_state.summary_output = None
            st.session_state.summary_input_text = ""
            st.session_state.pop('uploaded_file', None)
            st.session_state.pop('original_text', None)
            st.rerun()
