
import streamlit as st
from typing import Dict, List, Any
from utils.session import create_new_chat, reset_evaluation_state

def render_sidebar() -> str:
    """Render the sidebar with configuration and chat history."""
    with st.sidebar:
        st.header("Config")
        
        # Language selector
        selected_language = st.selectbox(
            "Select Language",
            options=list(st.session_state.SUPPORTED_LANGUAGES.keys()),
            index=list(st.session_state.SUPPORTED_LANGUAGES.keys()).index(st.session_state.selected_language)
        )
        
        # Update selected language if changed
        if selected_language != st.session_state.selected_language:
            st.session_state.selected_language = selected_language
            st.rerun()

        # Evaluation mode toggle
        eval_mode = st.toggle("Evaluation Mode", value=st.session_state.evaluation_mode)
        if eval_mode != st.session_state.evaluation_mode:
            st.session_state.evaluation_mode = eval_mode
            # Reset evaluation states when toggling
            reset_evaluation_state()
            st.rerun()
        
        if st.session_state.evaluation_mode:
            st.info("In evaluation mode, you'll be asked to provide ground truth answers for evaluation")
        
        st.header("Chat History")
        
        # New Chat button
        if st.button("New Chat", key="new_chat"):
            new_chat_id = create_new_chat(selected_language, st.session_state.SUPPORTED_LANGUAGES)
            st.session_state.current_chat_id = new_chat_id
            # Reset evaluation states for new chat
            reset_evaluation_state()
            st.rerun()
        
        # Display chat history
        st.divider()
        for chat_id, chat_data in sorted(
            st.session_state.chats.items(),
            key=lambda x: x[1]["timestamp"],
            reverse=True
        ):
            chat_title = chat_data["title"]
            if st.button(
                f"{chat_title}\n{chat_data['timestamp']}",
                key=f"chat_{chat_id}",
                use_container_width=True
            ):
                st.session_state.current_chat_id = chat_id
                # Reset evaluation states when switching chats
                reset_evaluation_state()
                st.rerun()
        
        if len(st.session_state.evaluation_results) > 0:
            st.header("Evaluation Dashboard")
            if st.button("View Evaluation Results", key="view_eval"):
                st.session_state.view_evaluation = True
                st.rerun()
        
        return selected_language