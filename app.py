
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Import modules
from config.settings import load_configuration
from utils.session import initialize_session_state
from utils.helpers import is_alarm_related_question
from models.rag import setup_rag_components, create_rag_chain
from evaluation.evaluator import GeminiRagasEvaluator
from ui.sidebar import render_sidebar
from ui.chat import display_chat, handle_user_input
from ui.evaluation import render_evaluation_dashboard, display_evaluation_results
from data.language import SUPPORTED_LANGUAGES

def main():
    """Main application logic."""
    # Load environment variables
    load_dotenv()
    
    # Streamlit page configuration
    st.set_page_config(page_title="NOC Assist RAG Chatbot", page_icon="🔍", layout="wide")
    
    # Load configuration
    config = load_configuration()
    
    # Check for viewing evaluation dashboard
    if "view_evaluation" in st.session_state and st.session_state.view_evaluation:
        render_evaluation_dashboard()
        if st.button("Back to Chat"):
            st.session_state.view_evaluation = False
            st.rerun()
        return

    st.title("RAN Ops Assist 🔍📡")
    st.info('Always follow Quality Points', icon="ℹ️")

    # Check for API key
    google_api_key = st.text_input("Enter Gemini API KEY", type="password")
    if not google_api_key:
        st.info("Please add your Google AI API key to continue.", icon="🗝️")
        return

    # Initialize session state with default language
    initialize_session_state("English", SUPPORTED_LANGUAGES)
    
    try:
        # Configure Gemini
        genai.configure(api_key=google_api_key)
        
        # Set up LLM
        llm = config['model_setup'](google_api_key)
        
        # Initialize evaluator
        evaluator = GeminiRagasEvaluator(google_api_key)
        
        # Setup RAG components
        retriever, all_docs = setup_rag_components()
        
        # Render sidebar and get selected language
        selected_language = render_sidebar()
        
        # Get current chat messages
        current_chat = st.session_state.chats[st.session_state.current_chat_id]
        messages = current_chat["messages"]
        
        # Create chains with selected language
        chains = create_rag_chain(llm, retriever, selected_language)
        
        # Display chat history
        display_chat(messages)

        # Handle evaluation display if evaluation is complete
        if st.session_state.evaluation_complete and st.session_state.evaluation_results_data:
            st.subheader("✅ Evaluation Results")
            display_evaluation_results(st.session_state.evaluation_results_data)

        # Handle evaluation input if waiting for ground truth
        elif st.session_state.awaiting_evaluation and st.session_state.current_evaluation_data:
            st.subheader("✅ Evaluation")
            with st.form("eval_form"):
                st.write("Please provide the ground truth for this query to evaluate the response:")
                ground_truth = st.text_area("Ground Truth Answer")
                
                submitted = st.form_submit_button("Submit & Evaluate")
                if submitted:
                    with st.spinner("Evaluating..."):
                        # Get stored evaluation data
                        eval_data = st.session_state.current_evaluation_data
                        
                        # Run evaluation
                        eval_results = evaluator.evaluate_rag(
                            question=eval_data["question"],
                            answer=eval_data["answer"],
                            contexts=eval_data["contexts"],
                            ground_truth=ground_truth
                        )
                        
                        # Add metadata
                        eval_results['question'] = eval_data["question"]
                        eval_results['answer'] = eval_data["answer"]
                        eval_results['retrieved_contexts'] = eval_data["contexts"]
                        eval_results['ground_truth'] = ground_truth
                        eval_results['timestamp'] = config['get_timestamp_iso']()
                        
                        # Store results
                        st.session_state.evaluation_results.append(eval_results)
                        
                        # Update state to show results
                        st.session_state.evaluation_complete = True
                        st.session_state.awaiting_evaluation = False
                        st.session_state.evaluation_results_data = eval_results
                        st.rerun()

        # Handle user input if not in middle of evaluation
        elif not st.session_state.awaiting_evaluation:
            handle_user_input(
                chains=chains, 
                is_alarm_related=is_alarm_related_question,
                evaluator=evaluator
            )
                
    except Exception as e:
        st.error(f"Error in application: {e}")

if __name__ == "__main__":
    main()