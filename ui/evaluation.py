
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any
import numpy as np
from datetime import datetime

def render_evaluation_dashboard() -> None:
    """Render the evaluation dashboard with visualization of results."""
    st.title("RAG System Evaluation Dashboard")
    
    if not st.session_state.evaluation_results:
        st.warning("No evaluation results available. Run some evaluations first!")
        return
    
    # Convert results to DataFrame for easier analysis
    eval_df = pd.DataFrame(st.session_state.evaluation_results)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg. Faithfulness", f"{eval_df['faithfulness'].mean():.2f}")
    with col2:
        st.metric("Avg. Relevance", f"{eval_df['relevance'].mean():.2f}")
    with col3:
        st.metric("Avg. Contextual Precision", f"{eval_df['contextual_precision'].mean():.2f}")
    with col4:
        if 'answer_correctness' in eval_df.columns:
            st.metric("Avg. Answer Correctness", f"{eval_df['answer_correctness'].mean():.2f}")
    
    # Create a radar chart for the average scores
    st.subheader("Average Scores Across All Evaluations")
    metrics = ['faithfulness', 'relevance', 'contextual_precision']
    if 'answer_correctness' in eval_df.columns:
        metrics.append('answer_correctness')
    
    avg_scores = [eval_df[metric].mean() for metric in metrics]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar chart
    x = np.arange(len(metrics))
    ax.bar(x, avg_scores, color='skyblue')
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel('Score')
    ax.set_title('Average Evaluation Scores')
    
    # Add score labels on top of bars
    for i, v in enumerate(avg_scores):
        ax.text(i, v + 0.02, f"{v:.2f}", ha='center')
    
    st.pyplot(fig)
    
    # Detailed results table
    st.subheader("Individual Evaluation Results")
    
    # Add a timestamp column in readable format
    eval_df['timestamp'] = pd.to_datetime(eval_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Select columns to display
    display_cols = ['timestamp', 'question'] + metrics + ['average_score']
    st.dataframe(eval_df[display_cols].sort_values('timestamp', ascending=False))
    
    # Option to export results
    if st.button("Export Results to CSV"):
        csv = eval_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"rag_evaluation_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

def display_evaluation_results(eval_results: Dict[str, Any]) -> None:
    """Display evaluation results in the UI."""
    st.success("✅ Evaluation completed!")
    
    # Display metrics with columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Faithfulness", f"{eval_results['faithfulness']:.2f}")
    with col2:
        st.metric("Relevance", f"{eval_results['relevance']:.2f}")
    with col3:
        st.metric("Contextual Precision", f"{eval_results['contextual_precision']:.2f}")
    with col4:
        if 'answer_correctness' in eval_results:
            st.metric("Answer Correctness", f"{eval_results['answer_correctness']:.2f}")
    
    # Display overall score
    st.metric("Overall Score", f"{eval_results['average_score']:.2f}")
    
    # Show retrieved contexts
    with st.expander("View Retrieved Contexts Used for Evaluation"):
        for i, context in enumerate(eval_results['retrieved_contexts']):
            st.markdown(f"**Context {i+1}:**")
            st.text(context)
    
    # Show ground truth comparison
    with st.expander("Compare Answer with Ground Truth"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("System Answer")
            st.write(eval_results['answer'])
        with col2:
            st.subheader("Ground Truth")
            st.write(eval_results['ground_truth'])
    
    # Continue button
    if st.button("Continue Chatting", key="continue_after_eval"):
        st.session_state.evaluation_complete = False
        st.session_state.awaiting_evaluation = False
        st.session_state.current_evaluation_data = None
        st.session_state.evaluation_results_data = None
        st.rerun()