import streamlit as st
from utils import generate_structured_flashcards


# --- CUSTOM CSS FOR FLASHCARDS ---
def inject_flashcard_css():
    """Injects custom CSS for modern flashcard styling"""
    st.markdown("""
    <style>
    /* ALL Primary buttons - Yellow background with dark text */
    button[kind="primary"] {
        background-color: #FFD700 !important;
        color: #1A1A1A !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #FFC700 !important;
        color: #1A1A1A !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* ALL Secondary buttons - Gray with NO yellow border by default */
    button[kind="secondary"] {
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #404040 !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    /* On hover - Yellow border and keep white text */
    button[kind="secondary"]:hover {
        border-color: #FFD700 !important;
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# --- FLASHCARD HELPER FUNCTIONS ---

def next_card():
    """Moves to the next card, looping back to the beginning if at the end."""
    if st.session_state.flashcard_type == "Conceptual (Q/A Flip)":
        st.session_state.card_side = 'Q'
    st.session_state.card_current_index = (st.session_state.card_current_index + 1) % len(st.session_state.flashcard_data)


def prev_card():
    """Moves to the previous card, looping to the last card if at the beginning."""
    num_cards = len(st.session_state.flashcard_data)
    if st.session_state.flashcard_type == "Conceptual (Q/A Flip)":
        st.session_state.card_side = 'Q'
    st.session_state.card_current_index = (st.session_state.card_current_index - 1 + num_cards) % num_cards


def flip_card():
    """Toggles the card side from Question to Answer and vice versa."""
    st.session_state.card_side = 'A' if st.session_state.card_side == 'Q' else 'Q'


def reset_flashcards():
    """Clears all flashcard-related state variables to return to the setup form."""
    st.session_state.pop('flashcard_data', None)
    st.session_state.pop('card_current_index', None)
    st.session_state.pop('card_side', None)
    st.session_state.pop('flashcard_topic', None)
    st.session_state.pop('flashcard_type', None)
    st.session_state.pop('flashcard_generating', None)


def display_flashcard_deck():
    """Renders flashcards with responsive carousel showing adjacent cards."""
    
    if not st.session_state.get('flashcard_data'):
        st.warning("No flashcard data available.")
        return

    inject_flashcard_css()

    data = st.session_state.flashcard_data
    current_idx = st.session_state.card_current_index
    current_card = data[current_idx]
    card_type = st.session_state.get('flashcard_type', 'Conceptual (Q/A Flip)')
    is_simple_mode = card_type == "Simple Explanation"
    is_front = st.session_state.card_side == 'Q'
    
    # Calculate adjacent cards (with wrapping)
    num_cards = len(data)
    prev_idx = (current_idx - 1) % num_cards
    next_idx = (current_idx + 1) % num_cards
    
    # Initialize animation direction state
    if 'last_card_index' not in st.session_state:
        st.session_state.last_card_index = 0
    if 'last_card_side' not in st.session_state:
        st.session_state.last_card_side = 'Q'
    
    # Determine slide direction
    going_forward = st.session_state.card_current_index > st.session_state.last_card_index
    flipping = st.session_state.card_current_index == st.session_state.last_card_index and st.session_state.card_side != st.session_state.last_card_side
    
    # Update tracking
    st.session_state.last_card_index = st.session_state.card_current_index
    st.session_state.last_card_side = st.session_state.card_side
    
    # Carousel CSS with responsive design
    st.markdown("""
    <style>
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-100px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }
    
    @keyframes flipIn {
        from {
            opacity: 0;
            transform: rotateX(90deg);
        }
        to {
            opacity: 1;
            transform: rotateX(0deg);
        }
    }
    
    .carousel-slide-right {
        animation: slideInRight 0.4s ease-out;
    }
    
    .carousel-slide-left {
        animation: slideInLeft 0.4s ease-out;
    }
    
    .carousel-flip {
        animation: flipIn 0.5s ease-out;
    }
    
    .side-card {
        opacity: 0.4;
        transform: scale(0.85);
        filter: blur(2px);
    }
    
    /* Hide side cards on mobile/small screens */
    @media (max-width: 768px) {
        .side-card-container {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Determine animation class
    if flipping:
        animation_class = "carousel-flip"
    elif going_forward:
        animation_class = "carousel-slide-right"
    else:
        animation_class = "carousel-slide-left"
    
    unique_key = f"{current_idx}_{st.session_state.card_side}"
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h2 style="color: #FFD700; margin-bottom: 0.5rem;">📇 {st.session_state.flashcard_topic}</h2>
        <p style="color: #999999; font-size: 1rem;">Card {current_idx + 1} of {len(data)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    progress = (current_idx + 1) / len(data)
    st.progress(progress)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # CAROUSEL with 3 cards visible (or 1 on mobile)
    carousel_container = st.container()
    
    with carousel_container:
        # Create 3-column layout for carousel (responsive)
        col_prev, col_current, col_next = st.columns([1, 3, 1])
        
        # Helper function to render a card
        def render_card(card, is_current=False, side='Q'):
            import html as html_lib
            
            border_color = "#FFD700" if side == 'Q' else "#4CAF50"
            card_class = animation_class if is_current else "side-card"
            font_size = '1.4rem' if is_current else '1rem'
            padding = '3rem' if is_current else '2rem'
            
            # Escape the text content
            question_escaped = html_lib.escape(card['question'])
            answer_escaped = html_lib.escape(card['answer'])
            
            if is_simple_mode:
                # SIMPLE EXPLANATION MODE - Show BOTH question and answer
                if is_current:
                    # Current card shows full question and answer
                    return f"""
                    <div class="{card_class}" style="
                        background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
                        border-radius: 20px;
                        border: 3px solid {border_color};
                        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
                        padding: {padding};
                        min-height: 350px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        overflow: hidden;
                    ">
                        <p style="color: #FFD700; font-weight: bold; font-size: 1.1rem; margin-bottom: 1rem; letter-spacing: 2px;">
                            {question_escaped}
                        </p>
                        <p style="color: #CCCCCC; font-size: 1.2rem; line-height: 1.8; text-align: center; margin-top: 1.5rem;">
                            {answer_escaped}
                        </p>
                    </div>
                    """
                else:
                    # Side cards show truncated question only
                    display_text = question_escaped[:40] + ('...' if len(question_escaped) > 40 else '')
                    return f"""
                    <div class="{card_class}" style="
                        background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
                        border-radius: 20px;
                        border: 3px solid {border_color};
                        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
                        padding: {padding};
                        min-height: 350px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        overflow: hidden;
                    ">
                        <p style="color: #FFD700; font-weight: bold; font-size: 0.9rem; margin-bottom: 0.8rem; letter-spacing: 2px;">
                            {display_text}
                        </p>
                    </div>
                    """
            else:
                # CONCEPTUAL MODE - Q/A Flip
                if side == 'Q':
                    label_text = "QUESTION"
                    label_color = "#FFD700"
                    content_text = question_escaped
                else:
                    label_text = "ANSWER"
                    label_color = "#4CAF50"
                    content_text = answer_escaped
                
                return f"""
                <div class="{card_class}" style="
                    background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
                    border-radius: 20px;
                    border: 3px solid {border_color};
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
                    padding: {padding};
                    min-height: 350px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <p style="color: {label_color}; font-weight: bold; font-size: 0.9rem; margin-bottom: 1rem; letter-spacing: 2px;">
                        {label_text}
                    </p>
                    <p style="color: #FFFFFF; font-size: {font_size}; line-height: 1.8; text-align: center;">
                        {content_text}
                    </p>
                </div>
                """
        
        # Previous card (peek) - hidden on mobile
        with col_prev:
            if num_cards > 1:
                st.markdown('<div class="side-card-container">', unsafe_allow_html=True)
                prev_card_html = render_card(data[prev_idx], is_current=False, side='Q')
                st.markdown(prev_card_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Current card (main) - always visible
        with col_current:
            current_card_html = render_card(current_card, is_current=True, side=st.session_state.card_side)
            st.markdown(current_card_html, unsafe_allow_html=True)
        
        # Next card (peek) - hidden on mobile
        with col_next:
            if num_cards > 1:
                st.markdown('<div class="side-card-container">', unsafe_allow_html=True)
                next_card_html = render_card(data[next_idx], is_current=False, side='Q')
                st.markdown(next_card_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation Controls
    if is_simple_mode:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("← Prev", on_click=prev_card, use_container_width=True, type="secondary", key="prev_btn")
        with col2:
            st.button("Next →", on_click=next_card, use_container_width=True, type="secondary", key="next_btn")
        with col3:
            st.button("✕ End", on_click=reset_flashcards, use_container_width=True, type="secondary", key="end_btn")
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #666666; font-size: 0.9rem;">
            💡 <strong>Tip:</strong> Use Prev/Next to navigate through explanations
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
        with col1:
            st.button("← Prev", on_click=prev_card, use_container_width=True, type="secondary", key="prev_btn")
        with col2:
            st.button("Next →", on_click=next_card, use_container_width=True, type="secondary", key="next_btn")
        with col3:
            flip_label = "🔄 Show Answer" if is_front else "🔄 Show Question"
            st.button(flip_label, on_click=flip_card, use_container_width=True, type="secondary", key="flip_btn")
        with col4:
            st.button("✕ End", on_click=reset_flashcards, use_container_width=True, type="secondary", key="end_btn")
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #666666; font-size: 0.9rem;">
            💡 <strong>Tip:</strong> Click the flip button to reveal the answer
        </div>
        """, unsafe_allow_html=True)


# --- MAIN FLASHCARD FUNCTION ---

def feature_generate_flashcards():
    """Handles the flashcard setup, generation, and flow management."""
    
    inject_flashcard_css()

    if 'flashcard_data' not in st.session_state:
        st.session_state.flashcard_data = None
    if 'card_current_index' not in st.session_state:
        st.session_state.card_current_index = 0
    if 'card_side' not in st.session_state:
        st.session_state.card_side = 'Q'
    if 'flashcard_generating' not in st.session_state:
        st.session_state.flashcard_generating = False

    if st.session_state.get('flashcard_data'):
        display_flashcard_deck()
        return

    # Custom header
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2rem;">📇 Generate Flashcards</h1>
        <p style="color: #CCCCCC; margin-top: 0.5rem; font-size: 1.1rem;">Strengthen memory through active recall with interactive cards</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CSS for container styling
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%) !important;
        border-radius: 20px !important;
        border: 2px solid #333333 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        padding: 2.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # SINGLE container - shows different content based on state
    with st.container(border=True):
        if st.session_state.flashcard_generating:
            # LOADING VIEW
            st.markdown("""
            <div style="
                padding: 2rem 1rem;
                text-align: center;
            ">
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
                <h3 style="color: #FFD700; margin: 0;">🔄 Generating Flashcards...</h3>
                <p style="color: #CCCCCC; margin-top: 0.5rem;">Please wait while we create your study materials</p>
            </div>
            
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Actually do the generation
            topic = st.session_state.flashcard_topic
            card_type = st.session_state.flashcard_type
            num_cards = st.session_state.get('flashcard_num_cards', 5)
            
            flashcard_data = generate_structured_flashcards(topic, num_cards)

            if flashcard_data and len(flashcard_data) > 0:
                valid_cards = [
                    card for card in flashcard_data 
                    if card.get('question') and card.get('answer')
                ]
                
                if valid_cards:
                    st.session_state.flashcard_data = valid_cards
                    st.session_state.card_current_index = 0
                    st.session_state.card_side = 'Q'
                    st.session_state.flashcard_generating = False
                    st.rerun()
                else:
                    st.session_state.flashcard_generating = False
                    st.rerun()
            else:
                st.session_state.flashcard_generating = False
                st.rerun()
        
        else:
            # SETUP FORM VIEW
            st.markdown('<h3 style="color: #FFD700; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.3rem;">🎴 Setup Your Flashcards</h3>', unsafe_allow_html=True)
            
            topic = st.text_area(
                "Enter the topic or notes for flashcard generation:",
                placeholder="e.g., Key dates and battles of the American Revolution, Python list comprehensions",
                height=120,
                key='flashcard_topic_input'
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                card_type = st.selectbox(
                    "Flashcard Type:",
                    ["Conceptual (Q/A Flip)", "Simple Explanation"],
                    key='flashcard_type_select',
                    help="Conceptual: Question/Answer flip cards | Simple: Direct explanations",
                    disabled=False 
                )
            st.markdown("""
                        <style>
/                       * Prevent editing in selectbox - make it select-only */
div[data-baseweb="select"] input {
    pointer-events: none !important;
    cursor: pointer !important;
}

/* Make the whole selectbox clickable */
div[data-baseweb="select"] {
    cursor: pointer !important;
}

/* Remove the input cursor */
div[data-baseweb="select"] input {
    caret-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)
            with col2:
                num_cards = st.number_input(
                    "Number of Flashcards:",
                    min_value=1,
                    max_value=20,
                    value=5,
                    key='num_cards_input',
                    help="Choose between 1-20 flashcards"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_left, col_center, col_right = st.columns([1, 2, 1])
            
            with col_center:
                if st.button("🚀 Generate Flashcards", type="primary", use_container_width=True, key="gen_flash_btn"):
                    if topic.strip():
                        st.session_state.flashcard_generating = True
                        st.session_state.flashcard_topic = topic
                        st.session_state.flashcard_type = card_type
                        st.session_state.flashcard_num_cards = num_cards
                        st.rerun()
                    else:
                        st.warning("⚠️ Please enter a topic or notes.")

