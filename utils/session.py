
import streamlit as st
import uuid
from typing import Dict, Any, List
from config.settings import get_timestamp

def generate_chat_id() -> str:
    """Generate a unique chat ID."""
    return str(uuid.uuid4())[:8]

def initialize_session_state(language: str, supported_languages: Dict[str, Dict[str, str]]) -> None:
    """Initialize session state with welcome message and chat management."""
    # Store supported languages in session state
    if "SUPPORTED_LANGUAGES" not in st.session_state:
        st.session_state.SUPPORTED_LANGUAGES = supported_languages

    if "chats" not in st.session_state:
        st.session_state.chats = {}

    if "current_chat_id" not in st.session_state:
        new_chat_id = generate_chat_id()
        st.session_state.current_chat_id = new_chat_id
        st.session_state.chats[new_chat_id] = {
            "messages": [{
                "role": "assistant",
                "content": supported_languages[language]["welcome"]
            }],
            "timestamp": get_timestamp(),
            "title": "New Chat"
        }

    if "selected_language" not in st.session_state:
        st.session_state.selected_language = language

    if "evaluation_results" not in st.session_state:
        st.session_state.evaluation_results = []

    if "evaluation_mode" not in st.session_state:
        st.session_state.evaluation_mode = False

    if "awaiting_evaluation" not in st.session_state:
        st.session_state.awaiting_evaluation = False

    if "current_evaluation_data" not in st.session_state:
        st.session_state.current_evaluation_data = None

    if "evaluation_complete" not in st.session_state:
        st.session_state.evaluation_complete = False

    if "evaluation_results_data" not in st.session_state:
        st.session_state.evaluation_results_data = None

    if "view_evaluation" not in st.session_state:
        st.session_state.view_evaluation = False

def update_chat_title(chat_id: str, messages: List[Dict[str, str]]) -> None:
    """Update chat title based on the first user message."""
    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
            st.session_state.chats[chat_id]["title"] = title
            break

def create_new_chat(language: str, supported_languages: Dict[str, Dict[str, str]]) -> str:
    """Create a new chat and return its ID."""
    new_chat_id = generate_chat_id()
    st.session_state.chats[new_chat_id] = {
        "messages": [{
            "role": "assistant",
            "content": supported_languages[language]["welcome"]
        }],
        "timestamp": get_timestamp(),
        "title": "New Chat"
    }
    return new_chat_id

def reset_evaluation_state() -> None:
    """Reset evaluation-related state variables."""
    st.session_state.awaiting_evaluation = False
    st.session_state.current_evaluation_data = None
    st.session_state.evaluation_complete = False
    st.session_state.evaluation_results_data = None