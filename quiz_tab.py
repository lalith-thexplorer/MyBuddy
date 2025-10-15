import streamlit as st
from utils import generate_structured_quiz


# --- CUSTOM CSS FOR QUIZ ---
def inject_custom_css():
    """Injects custom CSS for quiz button styling"""
    st.markdown("""
    <style>
    /* Make primary button text darker for better readability on yellow */
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
    
    /* Style ALL secondary buttons - Gray with gray border, yellow on hover */
    button[kind="secondary"], a[kind="secondary"] {
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #404040 !important;
        border-radius: 15px !important;
        padding: 1.2rem 1.5rem !important;
        font-size: 1.05rem !important;
        text-align: left !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-bottom: 0.75rem !important;
    }
    
    button[kind="secondary"]:hover, a[kind="secondary"]:hover {
        border-color: #FFD700 !important;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Download button specific styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        border-color: #FFD700 !important;
        transform: scale(1.02) !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Prevent typing in selectbox - make it dropdown-only */
    div[data-baseweb="select"] input {
        pointer-events: none !important;
        cursor: pointer !important;
        caret-color: transparent !important;
        user-select: none !important;
    }
    
    /* Make the selectbox clickable */
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
    </style>
    """, unsafe_allow_html=True)



# --- QUIZ HELPER FUNCTIONS ---

def check_answer(question_index, selected_option_index):
    """Checks the user's selected answer against the correct index."""
    if question_index >= len(st.session_state.quiz_data):
        st.error("Invalid question index")
        return
    
    if st.session_state.user_answers[question_index] is None:
        correct_index = st.session_state.quiz_data[question_index]['correct_index']
        is_correct = selected_option_index == correct_index
        st.session_state.user_answers[question_index] = {
            'selected': selected_option_index,
            'correct': is_correct
        }


def next_question():
    """Moves to the next question or finishes the quiz."""
    if st.session_state.quiz_current_index < len(st.session_state.quiz_data) - 1:
        st.session_state.quiz_current_index += 1
    else:
        st.session_state.quiz_finished = True


def show_quiz_results():
    """Displays the final score, accuracy, and download button."""
    correct_count = sum(1 for answer in st.session_state.user_answers if answer and answer['correct'])
    total_questions = len(st.session_state.quiz_data)
    accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    # Custom header for results
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2.5rem; margin-bottom: 0.5rem;">🎉 Quiz Complete!</h1>
        <p style="color: #999999; margin: 0; font-size: 1rem;">Great job finishing the quiz!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Score metrics in cards
    col_score, col_accuracy = st.columns(2)
    
    with col_score:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #333333;
            text-align: center;
        ">
            <p style="color: #999999; margin: 0; font-size: 0.9rem; margin-bottom: 0.5rem;">CORRECT ANSWERS</p>
            <p style="color: #FFD700; margin: 0; font-size: 2.5rem; font-weight: bold;">{correct_count}/{total_questions}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_accuracy:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #333333;
            text-align: center;
        ">
            <p style="color: #999999; margin: 0; font-size: 0.9rem; margin-bottom: 0.5rem;">ACCURACY</p>
            <p style="color: #FFD700; margin: 0; font-size: 2.5rem; font-weight: bold;">{accuracy:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance feedback - Centered and sleek
    performance_color = "#4CAF50" if accuracy >= 80 else "#42A5F5" if accuracy >= 60 else "#FF9800"
    performance_emoji = "🌟" if accuracy >= 80 else "👍" if accuracy >= 60 else "📚"
    performance_text = "Excellent work! You've mastered this topic!" if accuracy >= 80 else "Good job! Consider reviewing missed questions." if accuracy >= 60 else "Keep studying! Review the explanations and try again."
    
    col_perf_left, col_perf_center, col_perf_right = st.columns([0.5, 3, 0.5])
    
    with col_perf_center:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
            padding: 1.25rem 2rem;
            border-radius: 15px;
            border-left: 5px solid {performance_color};
            text-align: center;
            margin-bottom: 1.5rem;
        ">
            <p style="color: {performance_color}; margin: 0; font-size: 1.1rem; font-weight: 600;">
                {performance_emoji} {performance_text}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Topic and Difficulty - Small centered badge
    col_badge_left, col_badge_center, col_badge_right = st.columns([1, 2, 1])
    
    with col_badge_center:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%);
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            border: 1px solid #404040;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <p style="color: #FFD700; margin: 0; font-size: 0.9rem;">
                <strong>{st.session_state.quiz_topic}</strong> • {st.session_state.quiz_difficulty}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons - Same height with proper alignment
    st.markdown("""
    <style>
    /* Ensure download button matches primary button exactly */
    div[data-testid="column"] .stDownloadButton {
        display: flex;
        align-items: stretch;
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #2A2A2A 0%, #1E1E1E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stDownloadButton button:hover {
        border-color: #FFD700 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3) !important;
    }
    
    /* Match primary button height */
    div[data-testid="column"] button {
        min-height: 3.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Start New Quiz", type="primary", use_container_width=True, key="new_quiz_btn"):
            reset_quiz_state()
            st.rerun()
    
    with col2:
        # Generate downloadable results
        results_text = generate_quiz_results_text(correct_count, total_questions, accuracy)
        
        st.download_button(
            label="📥 Download Results",
            data=results_text,
            file_name=f"quiz_results_{st.session_state.quiz_topic.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_results_btn"
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)


def generate_quiz_results_text(correct_count, total_questions, accuracy):
    """Generates a formatted text file with quiz results."""
    
    results = f"""
╔════════════════════════════════════════════════════════════════╗
║                    QUIZ RESULTS - MyBuddy                      ║
╚════════════════════════════════════════════════════════════════╝

Topic: {st.session_state.quiz_topic}
Difficulty: {st.session_state.quiz_difficulty}
Date: {st.session_state.get('quiz_date', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCORE SUMMARY:
  Correct Answers: {correct_count} / {total_questions}
  Accuracy: {accuracy:.1f}%
  
Performance: {"🌟 Excellent!" if accuracy >= 80 else "👍 Good!" if accuracy >= 60 else "📚 Keep Practicing!"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DETAILED RESULTS:

"""
    
    # Add each question and answer
    for idx, question_data in enumerate(st.session_state.quiz_data):
        user_answer = st.session_state.user_answers[idx]
        is_correct = user_answer and user_answer['correct']
        
        results += f"\nQuestion {idx + 1}:\n"
        results += f"{question_data['question']}\n\n"
        
        # Show all options
        for opt_idx, option in enumerate(question_data['options']):
            marker = ""
            if opt_idx == question_data['correct_index']:
                marker = "✓ (Correct Answer)"
            elif user_answer and opt_idx == user_answer['selected']:
                marker = "✗ (Your Answer)" if not is_correct else "✓ (Your Answer)"
            
            results += f"  {chr(65 + opt_idx)}. {option} {marker}\n"
        
        results += f"\nResult: {'✅ Correct' if is_correct else '❌ Incorrect'}\n"
        results += f"Explanation: {question_data['explanation']}\n"
        results += "\n" + "─" * 64 + "\n"
    
    results += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated by MyBuddy - AI Study Companion
Keep learning and improving! 🚀
"""
    
    return results

def reset_quiz_state():
    """Clears all quiz-related session state variables."""
    st.session_state.pop('quiz_data', None)
    st.session_state.pop('quiz_current_index', None)
    st.session_state.pop('user_answers', None)
    st.session_state.pop('quiz_started', None)
    st.session_state.pop('quiz_finished', None)
    st.session_state.pop('quiz_topic', None)
    st.session_state.pop('quiz_difficulty', None)
    st.session_state.pop('quiz_generating', None)


def display_quiz_question():
    """Renders the current question card, options, feedback, and navigation."""
    
    if not st.session_state.get('quiz_data'):
        st.warning("No quiz data loaded. Please start a quiz.")
        return

    if st.session_state.get('quiz_finished', False):
        show_quiz_results()
        return

    q_index = st.session_state.quiz_current_index
    question_data = st.session_state.quiz_data[q_index]
    is_answered = st.session_state.user_answers[q_index] is not None
    
    # Progress bar
    progress = (q_index + 1) / len(st.session_state.quiz_data)
    st.progress(progress, text=f"Question {q_index + 1} of {len(st.session_state.quiz_data)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- EVERYTHING IN ONE CONTAINER ---
    with st.container(border=True):
        # Question header
        st.markdown(f"""
        <h3 style="color: #FFD700; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.1rem; font-weight: 600;">
            Question {q_index + 1}
        </h3>
        <p style="color: #FFFFFF; font-size: 1.3rem; margin-bottom: 2rem; line-height: 1.8;">
            {question_data['question']}
        </p>
        <p style="color: #CCCCCC; font-size: 1rem; margin-bottom: 1rem; font-weight: 600;">
            Choose your answer:
        </p>
        """, unsafe_allow_html=True)

        # Options
        options = question_data['options']
        correct_index = question_data['correct_index']
        
        for idx, option in enumerate(options):
            is_selected = is_answered and st.session_state.user_answers[q_index]['selected'] == idx
            is_correct_option = idx == correct_index
            
            if not is_answered:
                button_label = f"{chr(65 + idx)}.  {option}"
                
                if st.button(
                    button_label,
                    key=f"quiz_opt_{q_index}_{idx}",
                    use_container_width=True,
                    type="secondary",
                    disabled=False
                ):
                    check_answer(q_index, idx)
                    st.rerun()
            
            else:
                if is_correct_option:
                    bg_color = "#1B5E20"
                    border_color = "#4CAF50"
                    icon = "✅"
                elif is_selected and not is_correct_option:
                    bg_color = "#B71C1C"
                    border_color = "#EF5350"
                    icon = "❌"
                else:
                    bg_color = "#2A2A2A"
                    border_color = "#404040"
                    icon = ""
                
                option_html = f"""
                <div style="
                    background-color: {bg_color};
                    padding: 1.2rem 1.5rem;
                    margin-bottom: 0.75rem;
                    border-radius: 15px;
                    border: 2px solid {border_color};
                    color: #FFFFFF;
                    font-size: 1.05rem;
                    pointer-events: none;
                    user-select: none;
                ">
                    {icon} <strong>{chr(65 + idx)}.</strong> {option}
                </div>
                """
                st.markdown(option_html, unsafe_allow_html=True)

    # Feedback Section (OUTSIDE the container)
    if is_answered:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.user_answers[q_index]['correct']:
            st.success("✅ **Correct!** Well done.")
        else:
            correct_answer = options[correct_index]
            st.error(f"❌ **Incorrect.** The correct answer was: **{chr(65 + correct_index)}. {correct_answer}**")
        
        explanation_card = f"""
        <div style="
            background: linear-gradient(135deg, #1A1A1A 0%, #252525 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 4px solid #FFD700;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        ">
            <h5 style="color: #FFD700; margin-top: 0; margin-bottom: 1rem; font-size: 1.1rem;">
                💡 Explanation
            </h5>
            <p style="color: #CCCCCC; margin: 0; line-height: 1.7; font-size: 1rem;">
                {question_data['explanation']}
            </p>
        </div>
        """
        st.markdown(explanation_card, unsafe_allow_html=True)
        
        is_last_question = q_index >= len(st.session_state.quiz_data) - 1
        
        col_spacer, col_button = st.columns([2.5, 1])
        
        with col_button:
            if is_last_question:
                btn_label = "Finish 🏁"
                btn_key = f"finish_q{q_index}"
            else:
                btn_label = "Next →"
                btn_key = f"next_q{q_index}"
            
            st.markdown("""
            <style>
            div[data-testid="column"]:last-child button[kind="primary"] {
                border-radius: 25px !important;
                padding: 0.75rem 1.5rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            if st.button(
                btn_label,
                type="primary",
                use_container_width=True,
                key=btn_key
            ):
                next_question()
                st.rerun()

# --- MAIN QUIZ FUNCTION ---

def feature_generate_quiz():
    """Handles the quiz setup, generation, and flow management."""
    
    inject_custom_css()
    
    # Initialize state
    if 'quiz_generating' not in st.session_state:
        st.session_state.quiz_generating = False
    
    quiz_started = st.session_state.get('quiz_started', False)

    # Custom header
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2rem;">🧠 Generate Quiz</h1>
        <p style="color: #CCCCCC; margin-top: 0.5rem; font-size: 1.1rem;">Interactive exam-style self-testing with instant feedback</p>
    </div>
    """, unsafe_allow_html=True)

    if not quiz_started or st.session_state.get('quiz_finished', False):
        if st.session_state.get('quiz_finished', False):
            show_quiz_results()
            return 

        # Loading state
        if st.session_state.quiz_generating:
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
                    <h3 style="color: #FFD700; margin: 0;">🔄 Generating Quiz...</h3>
                    <p style="color: #CCCCCC; margin-top: 0.5rem;">Please wait while we create your questions</p>
                </div>
                
                <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                </style>
                """, unsafe_allow_html=True)
            
            topic = st.session_state.quiz_topic
            difficulty = st.session_state.quiz_difficulty
            num_questions = st.session_state.get('quiz_num_questions', 5)
            
            quiz_data = generate_structured_quiz(topic, difficulty, num_questions)

            if quiz_data and len(quiz_data) > 0:
                st.session_state.quiz_data = quiz_data
                st.session_state.quiz_current_index = 0
                st.session_state.user_answers = [None] * len(quiz_data)
                st.session_state.quiz_finished = False
                st.session_state.quiz_started = True
                st.session_state.quiz_generating = False
                st.rerun()
            else:
                st.session_state.quiz_generating = False
                st.session_state.quiz_started = False
                st.rerun()
            
            return

        # Setup Form
        with st.container(border=True):
            st.markdown('<h3 style="color: #FFD700; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.3rem;">📝 Quiz Setup</h3>', unsafe_allow_html=True)
            
            topic = st.text_area(
                "Enter the topic for the quiz:",
                placeholder="e.g., Photosynthesis, World War II, Python Data Structures",
                height=100,
                key='quiz_topic_input'
            )
            
            col_diff, col_count = st.columns(2)
            with col_diff:
                difficulty = st.selectbox(
                    "Select Difficulty:",
                    ["Basic", "Intermediate", "Advanced"],
                    index=0,
                    key='quiz_difficulty_select',
                    help="Basic: Simple recall | Intermediate: Conceptual | Advanced: Application"
                )
            with col_count:
                num_questions = st.number_input(
                    "Number of Questions:",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key='quiz_num_questions_input',
                    help="Choose between 1-10 questions"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Start Quiz", type="primary", use_container_width=True, key="start_quiz_btn"):
                    if topic.strip():
                        st.session_state.quiz_generating = True
                        st.session_state.quiz_topic = topic
                        st.session_state.quiz_difficulty = difficulty
                        st.session_state.quiz_num_questions = num_questions
                        st.rerun()
                    else:
                        st.warning("⚠️ Please enter a topic to start the quiz.")
    
    else:
        display_quiz_question()
