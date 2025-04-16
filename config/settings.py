
import os
from datetime import datetime
from typing import Dict, Any, Callable
from langchain_google_genai import ChatGoogleGenerativeAI

def get_timestamp() -> str:
    """Get current timestamp in readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def get_timestamp_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def setup_model(google_api_key: str) -> ChatGoogleGenerativeAI:
    """Set up and return the language model."""
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        convert_system_message_to_human=True
    )

def load_configuration() -> Dict[str, Any]:
    """Load and return application configuration."""
    return {
        'logo_path': os.getenv('LOGO_PATH', ''),
        'pdf_dir': "pdf files",
        'chunk_size': 300,
        'chunk_overlap': 50,
        'get_timestamp': get_timestamp,
        'get_timestamp_iso': get_timestamp_iso,
        'model_setup': setup_model
    }