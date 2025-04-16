
import streamlit as st
from typing import Dict, List, Any, Callable
import time
from utils.session import update_chat_title
from utils.helpers import format_chat_history

def display_chat(messages: List[Dict[str, str]]) -> None:
    """Display chat history in the UI."""
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(chains: Dict[str, Any], is_alarm_related: Callable, evaluator: Any = None) -> None:
    """Handle user input and generate response."""
    if prompt := st.chat_input("What would you like to know about NOC operations?"):
        # Get current chat data
        current_chat_id = st.session_state.current_chat_id
        current_chat = st.session_state.chats[current_chat_id]
        messages = current_chat["messages"]
        
        # Add user message to chat
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.spinner("Processing your query..."):
                # Update chat title if this is the first user message
                update_chat_title(current_chat_id, messages)
                
                # Format chat history
                chat_history = format_chat_history(messages)
                
                # Choose appropriate chain based on question type
                chain_type = 'alarm' if is_alarm_related(prompt) else 'general'
                
                response = chains[chain_type].invoke({
                    "input": prompt,
                    "chat_history": chat_history
                })
                
                # Store the retrieved documents for evaluation
                retrieved_contexts = [doc.page_content for doc in response['context']]
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(response['answer'])
                
                # Store assistant response
                messages.append({
                    "role": "assistant", 
                    "content": response['answer']
                })
                
                # If in evaluation mode, prepare for evaluation
                if st.session_state.evaluation_mode and evaluator:
                    # Store data for evaluation
                    st.session_state.current_evaluation_data = {
                        "question": prompt,
                        "answer": response['answer'],
                        "contexts": retrieved_contexts
                    }
                    st.session_state.awaiting_evaluation = True
                    st.rerun()

        except Exception as e:
            st.error(f"An error occurred while generating response: {e}")