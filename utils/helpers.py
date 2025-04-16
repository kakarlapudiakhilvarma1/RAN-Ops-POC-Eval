
from typing import List, Dict, Any

def is_alarm_related_question(question: str) -> bool:
    """Check if the question is related to alarms or technical issues."""
    alarm_keywords = [
        'alarm', 'alert', 'error', 'failure', 'maintenance', 'connection',
        'unit', 'rf', 'radio', 'network', 'fault', 'down', 'offline', 'missing'
    ]
    return any(keyword in question.lower() for keyword in alarm_keywords)

def is_history_related_question(question: str) -> bool:
    """Check if the question is about chat history."""
    history_keywords = [
        'previous', 'earlier', 'before', 'last time', 'history',
        'what did', 'what was', 'what were', 'asked', 'said'
    ]
    return any(keyword in question.lower() for keyword in history_keywords)

def format_chat_history(messages: List[Dict[str, str]]) -> str:
    """Format chat history into a string for the prompt."""
    formatted_history = []
    for msg in messages[1:]:  # Skip the initial greeting
        role = "Human" if msg["role"] == "user" else "Assistant"
        formatted_history.append(f"{role}: {msg['content']}")
    return "\n".join(formatted_history)