import streamlit as st
import os
import json 
import requests
import time
import pdfplumber
from io import BytesIO

# --- Configuration for Gemini API ---
try:
    GEMINI_API_KEY = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
if not GEMINI_API_KEY:
    st.error("⚠️ **GOOGLE_API_KEY not found!**")
    st.info("""
    **How to fix:**
    1. Create a file: `.streamlit/secrets.toml` in your project folder
    2. Add this line: `GOOGLE_API_KEY = "your-api-key-here"`
    3. Get your free API key from: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
    """)
    st.stop()

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
MAX_RETRIES = 5
BASE_DELAY = 2

# --- JSON Schema for Structured Quiz Output ---
QUIZ_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "question": {"type": "STRING", "description": "The multiple choice question text."},
            "options": {
                "type": "ARRAY",
                "items": {"type": "STRING"},
                "description": "An array of exactly four possible answers."
            },
            "correct_index": {"type": "INTEGER", "description": "The zero-based index (0, 1, 2, or 3) of the correct answer in the options array."},
            "explanation": {"type": "STRING", "description": "A concise explanation of why the correct answer is right."}
        },
        "required": ["question", "options", "correct_index", "explanation"]
    }
}

FLASHCARD_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "question": {"type": "STRING", "description": "The front side of the flashcard, acting as the prompt or concept."},
            "answer": {"type": "STRING", "description": "The back side of the flashcard, containing the definition or key information."}
        },
        "required": ["question", "answer"]
    }
}

# --- Utility Functions ---

def generate_content_with_backoff(payload):
    """Makes a request to the Gemini API with exponential backoff for retries."""
    if not GEMINI_API_KEY:
        st.error("Gemini API key not found.")
        return None

    headers = {'Content-Type': 'application/json'}
    params = {'key': GEMINI_API_KEY}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                GEMINI_API_URL,
                headers=headers,
                params=params,
                data=json.dumps(payload),
                timeout=60,
            )
            response.raise_for_status() 

            result = response.json()
            
            if 'candidates' not in result or not result['candidates']:
                st.error("AI response failed: No candidates returned.")
                return None
            
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** attempt)
                time.sleep(delay)
            else:
                detail = ""
                response = getattr(e, "response", None)
                if response is not None:
                    detail = f" (HTTP {response.status_code}: {response.text[:300]})"
                st.error(f"Max retries reached. API request failed.{detail}")
                return None
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            st.error(f"Error processing API response: {e}")
            return None
    return None

def generate_structured_quiz(topic, difficulty, num_questions):
    """Generates structured quiz data using the Gemini API's JSON output capability."""
    if not GEMINI_API_KEY:
        st.error("Gemini API key not found.")
        return None

    system_prompt = f"""You are 'MyBuddy', an AI exam generation engine. Generate {num_questions} multiple-choice questions on '{topic}' at '{difficulty}' level. Each question must have exactly four options."""
    
    payload = {
        "contents": [{"parts": [{"text": f"Generate {num_questions} MCQs about {topic}."}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": QUIZ_SCHEMA
        },
        "model": "gemini-2.5-flash"
    }

    headers = {'Content-Type': 'application/json'}
    params = {'key': GEMINI_API_KEY}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                GEMINI_API_URL,
                headers=headers,
                params=params,
                data=json.dumps(payload),
                timeout=60,
            )
            response.raise_for_status()
            
            result = response.json()
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            quiz_data = json.loads(raw_text)
            
            return quiz_data if quiz_data else None

        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(BASE_DELAY * (2 ** attempt))
            else:
                st.error("Max retries reached. Quiz generation failed.")
                return None
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            st.error(f"Error parsing quiz data: {e}")
            return None
    return None

def generate_structured_flashcards(topic, num_cards):
    """Generates structured flashcard data using the Gemini API's JSON output capability."""
    if not GEMINI_API_KEY:
        st.error("Gemini API key not found.")
        return None

    system_prompt = f"""You are 'MyBuddy', an AI study companion. Generate exactly {num_cards} flashcards based on '{topic}'. Each must have a 'question' (concept) and an 'answer' (definition)."""
    
    payload = {
        "contents": [{"parts": [{"text": f"Generate {num_cards} flashcards about {topic}."}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": FLASHCARD_SCHEMA
        },
        "model": "gemini-2.5-flash"
    }

    headers = {'Content-Type': 'application/json'}
    params = {'key': GEMINI_API_KEY}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                GEMINI_API_URL,
                headers=headers,
                params=params,
                data=json.dumps(payload),
                timeout=60,
            )
            response.raise_for_status()
            
            result = response.json()
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            card_data = json.loads(raw_text)

            return card_data if card_data else None

        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(BASE_DELAY * (2 ** attempt))
            else:
                st.error("Max retries reached. Flashcard generation failed.")
                return None
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            st.error(f"Error parsing flashcard data: {e}")
            return None
    return None

def extract_text_from_file(uploaded_file):
    """Extracts text from an uploaded file (PDF or TXT)."""
    if uploaded_file is None:
        st.error("No file uploaded.")
        return None

    # Ensure repeated attempts read from the beginning of the in-memory file.
    try:
        uploaded_file.seek(0)
    except Exception:
        pass
    
    file_type = (uploaded_file.type or "").lower()
    file_name = (getattr(uploaded_file, "name", "") or "").lower()

    # Some browsers/uploader flows return a generic MIME type.
    if not file_type or file_type == "application/octet-stream":
        if file_name.endswith(".pdf"):
            file_type = "application/pdf"
        elif file_name.endswith(".txt"):
            file_type = "text/plain"
    
    if file_type == "text/plain":
        try:
            raw_bytes = uploaded_file.getvalue()
            try:
                return raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                # Fallback for legacy encodings.
                return raw_bytes.decode("latin-1")
        except Exception as e:
            st.error(f"Error reading text file: {e}")
            return None
        
    elif file_type == "application/pdf":
        try:
            file_bytes = uploaded_file.getvalue()
            if not file_bytes:
                st.error("Uploaded PDF appears to be empty.")
                return None

            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                text_chunks = []
                for page in pdf.pages[:10]:  # First 10 pages
                    page_text = page.extract_text() or ""

                    # Fallback: reconstruct text from extracted words when line extraction fails.
                    if not page_text.strip():
                        words = page.extract_words() or []
                        if words:
                            page_text = " ".join(word.get("text", "") for word in words)

                    if page_text and page_text.strip():
                        text_chunks.append(page_text.strip())

                text = "\n\n".join(text_chunks).strip()
                if text:
                    return text

                st.error("No selectable text was found in the PDF. It may be a scanned/image-only PDF.")
                return None
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            return None
    else:
        st.error(f"Unsupported file type. Please upload PDF or TXT files only.")
        return None
