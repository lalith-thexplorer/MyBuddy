import streamlit as st
from utils import generate_structured_flashcards


# --- CUSTOM CSS FOR FLASHCARDS ---
def inject_flashcard_css():
    """Injects custom CSS for modern flashcard styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    :root {
        --deck-bg: rgba(15, 22, 34, 0.92);
        --deck-bg-2: rgba(20, 30, 44, 0.96);
        --deck-line: rgba(255, 255, 255, 0.08);
    }

    .stApp, .main, body {
        background:
            radial-gradient(circle at top left, rgba(255, 210, 74, 0.10), transparent 24%),
            radial-gradient(circle at top right, rgba(103, 232, 208, 0.10), transparent 20%),
            linear-gradient(180deg, #081018, #060b12) !important;
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.03em;
    }

    body, p, div, span, button, input, textarea, select {
        font-family: 'Manrope', sans-serif;
    }

    /* ALL Primary buttons - Yellow background with dark text */
    button[kind="primary"] {
        background: linear-gradient(135deg, #ffe17a, #ffbf2f) !important;
        color: #111827 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 1.02rem !important;
        transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease !important;
        box-shadow: 0 18px 34px rgba(255, 191, 47, 0.22) !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 26px 42px rgba(255, 191, 47, 0.32) !important;
        filter: brightness(1.03) saturate(1.05) !important;
    }
    
    /* ALL Secondary buttons - Gray with NO yellow border by default */
    button[kind="secondary"] {
        background: linear-gradient(135deg, rgba(28, 38, 52, 0.96), rgba(16, 24, 36, 0.96)) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 18px !important;
        padding: 0.68rem 1.2rem !important;
        font-size: 1rem !important;
        transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease !important;
    }
    
    /* On hover - Yellow border and keep white text */
    button[kind="secondary"]:hover {
        border-color: rgba(255, 210, 74, 0.55) !important;
        background: linear-gradient(135deg, rgba(28, 38, 52, 0.96), rgba(16, 24, 36, 0.96)) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25) !important;
    }

    .deck-shell {
        perspective: 1800px;
    }

    .deck-card {
        position: relative;
        transform-style: preserve-3d;
        transition: transform 760ms cubic-bezier(0.2, 0.8, 0.15, 1), opacity 260ms ease, filter 260ms ease;
        will-change: transform;
    }

    .deck-card.current-slide-next {
        animation: deckEnterNext 720ms cubic-bezier(0.2, 0.8, 0.15, 1);
    }

    .deck-card.current-slide-prev {
        animation: deckEnterPrev 720ms cubic-bezier(0.2, 0.8, 0.15, 1);
    }

    .deck-card.current-flip {
        animation: deckFlipPulse 700ms cubic-bezier(0.2, 0.8, 0.15, 1);
    }

    .deck-card.side-peek-left {
        transform: translateX(10px) rotateY(12deg) scale(0.90);
        opacity: 0.42;
        filter: blur(1px) saturate(0.8);
    }

    .deck-card.side-peek-right {
        transform: translateX(-10px) rotateY(-12deg) scale(0.90);
        opacity: 0.42;
        filter: blur(1px) saturate(0.8);
    }

    .flip-shell {
        position: relative;
        width: 100%;
        min-height: 380px;
        perspective: 1800px;
    }

    .flip-inner {
        position: relative;
        width: 100%;
        min-height: 380px;
        transform-style: preserve-3d;
        transition: transform 860ms cubic-bezier(0.2, 0.8, 0.15, 1);
    }

    .flip-inner.is-flipped {
        transform: rotateY(180deg);
    }

    .flip-face {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        backface-visibility: hidden;
        border-radius: 28px;
        overflow: hidden;
        border: 1px solid var(--deck-line);
        background: linear-gradient(180deg, var(--deck-bg), var(--deck-bg-2));
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.42);
    }

    .flip-face::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), transparent 35%, transparent 65%, rgba(255, 255, 255, 0.04));
        pointer-events: none;
    }

    .flip-face.back {
        transform: rotateY(180deg);
    }

    .card-title-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        width: fit-content;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        background: rgba(255, 210, 74, 0.10);
        border: 1px solid rgba(255, 210, 74, 0.18);
        color: #fff2b4;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .card-content {
        position: relative;
        z-index: 1;
    }

    @keyframes deckEnterNext {
        0% { opacity: 0; transform: translateX(28px) scale(0.96); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }

    @keyframes deckEnterPrev {
        0% { opacity: 0; transform: translateX(-28px) scale(0.96); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }

    @keyframes deckFlipPulse {
        0% { transform: scale(0.985); }
        45% { transform: scale(1.015); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)


# --- FLASHCARD HELPER FUNCTIONS ---

def next_card():
    """Moves to the next card, looping back to the beginning if at the end."""
    if st.session_state.flashcard_type == "Conceptual (Q/A Flip)":
        st.session_state.card_side = 'Q'
    st.session_state.flashcard_motion = 'next'
    st.session_state.card_current_index = (st.session_state.card_current_index + 1) % len(st.session_state.flashcard_data)


def prev_card():
    """Moves to the previous card, looping to the last card if at the beginning."""
    num_cards = len(st.session_state.flashcard_data)
    if st.session_state.flashcard_type == "Conceptual (Q/A Flip)":
        st.session_state.card_side = 'Q'
    st.session_state.flashcard_motion = 'prev'
    st.session_state.card_current_index = (st.session_state.card_current_index - 1 + num_cards) % num_cards


def flip_card():
    """Toggles the card side from Question to Answer and vice versa."""
    st.session_state.flashcard_motion = 'flip'
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
    if 'flashcard_motion' not in st.session_state:
        st.session_state.flashcard_motion = None
    
    # Determine slide direction
    going_forward = st.session_state.card_current_index > st.session_state.last_card_index
    flipping = st.session_state.card_current_index == st.session_state.last_card_index and st.session_state.card_side != st.session_state.last_card_side
    motion = st.session_state.get('flashcard_motion')
    
    # Update tracking
    st.session_state.last_card_index = st.session_state.card_current_index
    st.session_state.last_card_side = st.session_state.card_side
    st.session_state.flashcard_motion = None
    
    # Determine animation class
    if motion == 'flip' or flipping:
        animation_class = "current-flip"
    elif motion == 'next' or going_forward:
        animation_class = "current-slide-next"
    else:
        animation_class = "current-slide-prev"
    
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
        def render_card(card, is_current=False, side='Q', peek_side=None):
            import html as html_lib
            
            border_color = "#FFD700" if side == 'Q' else "#4CAF50"
            if is_current:
                card_class = f"deck-card {animation_class}"
            elif peek_side == 'left':
                card_class = "deck-card side-peek-left"
            elif peek_side == 'right':
                card_class = "deck-card side-peek-right"
            else:
                card_class = "deck-card"
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
                return f"""
                <div class="{card_class}">
                    <div class="flip-shell">
                        <div class="flip-inner {'is-flipped' if side == 'A' else ''}">
                            <div class="flip-face front" style="padding: {padding}; align-items: center; text-align: center; min-height: 380px;">
                                <div class="card-content" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 380px; text-align: center;">
                                    <div class="card-title-badge">QUESTION</div>
                                    <p style="color: #FFFFFF; font-size: {font_size}; line-height: 1.8; text-align: center; margin: 1rem 0 0 0;">
                                        {question_escaped}
                                    </p>
                                </div>
                            </div>
                            <div class="flip-face back" style="padding: {padding}; align-items: center; text-align: center; min-height: 380px;">
                                <div class="card-content" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 380px; text-align: center;">
                                    <div class="card-title-badge">ANSWER</div>
                                    <p style="color: #D7E1EE; font-size: {font_size}; line-height: 1.8; text-align: center; margin: 1rem 0 0 0;">
                                        {answer_escaped}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """
        
        # Previous card (peek) - hidden on mobile
        with col_prev:
            if num_cards > 1:
                st.markdown('<div class="side-card-container">', unsafe_allow_html=True)
                prev_card_html = render_card(data[prev_idx], is_current=False, side='Q', peek_side='left')
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
                next_card_html = render_card(data[next_idx], is_current=False, side='Q', peek_side='right')
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
    if 'flashcard_motion' not in st.session_state:
        st.session_state.flashcard_motion = None

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
/* Prevent editing in selectbox - make it select-only */
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

