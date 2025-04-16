
import streamlit as st
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiRagasEvaluator:
    def __init__(self, google_api_key: str):
        genai.configure(api_key=google_api_key)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )

    def evaluate_faithfulness(self, answer: str, contexts: List[str]) -> float:
        """
        Evaluate if the answer is faithful to the given contexts
        Returns a score between 0 and 1
        """
        prompt = f"""
        You are a critical evaluator assessing the faithfulness of an answer to provided context.

        Context:
        {' '.join(contexts)}

        Answer:
        {answer}

        Task:
        On a scale of 0 to 1, where 1 means the answer is completely faithful to the context and 0 means it contains hallucinations or unsupported information:
        1. Analyze each claim or statement in the answer
        2. Check if it's directly supported by the context
        3. Determine if there are any unsupported extrapolations
        4. Provide a single numerical score between 0 and 1

        Return only the numerical score without any explanation.
        """
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        score_text = response.text.strip()
        try:
            score = float(score_text)
            return max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
        except ValueError:
            st.error(f"Failed to parse faithfulness score: {score_text}")
            return 0.5  # Default middle score

    def evaluate_relevance(self, question: str, contexts: List[str]) -> float:
        """
        Evaluate if the retrieved contexts are relevant to the question
        Returns a score between 0 and 1
        """
        prompt = f"""
        You are evaluating the relevance of retrieved documents to a question.

        Question:
        {question}

        Retrieved documents:
        {' '.join(contexts)}

        Task:
        On a scale of 0 to 1, where 1 means the documents are highly relevant to answering the question and 0 means they are completely irrelevant:
        1. Assess how well the documents address the information needs in the question
        2. Consider whether key information required to answer the question is present
        3. Ignore extraneous information if the core relevant content is present
        4. Provide a single numerical score between 0 and 1

        Return only the numerical score without any explanation.
        """
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        score_text = response.text.strip()
        try:
            score = float(score_text)
            return max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
        except ValueError:
            st.error(f"Failed to parse relevance score: {score_text}")
            return 0.5  # Default middle score

    def evaluate_contextual_precision(self, answer: str, question: str, contexts: List[str]) -> float:
        """
        Evaluate if the answer uses relevant parts of the contexts efficiently
        Returns a score between 0 and 1
        """
        prompt = f"""
        You are evaluating the contextual precision of an answer.

        Question:
        {question}

        Answer:
        {answer}

        Contexts:
        {' '.join(contexts)}

        Task:
        On a scale of 0 to 1, where 1 means the answer efficiently uses only relevant parts of the context and 0 means it includes lots of irrelevant information:
        1. Determine how much of the context used in the answer was directly relevant to the question
        2. Check if the answer contains information from the context that doesn't help answer the question
        3. Assess whether the answer is concise while covering the necessary information
        4. Provide a single numerical score between 0 and 1

        Return only the numerical score without any explanation.
        """
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        score_text = response.text.strip()
        try:
            score = float(score_text)
            return max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
        except ValueError:
            st.error(f"Failed to parse contextual precision score: {score_text}")
            return 0.5  # Default middle score

    def evaluate_answer_correctness(self, answer: str, ground_truth: str) -> float:
        """
        Evaluate if the answer is correct compared to the ground truth
        Returns a score between 0 and 1
        """
        prompt = f"""
        You are evaluating the correctness of an answer against a known ground truth.

        Answer to evaluate:
        {answer}

        Ground truth:
        {ground_truth}

        Task:
        On a scale of 0 to 1, where 1 means the answer completely matches the ground truth in meaning and information and 0 means it's completely incorrect:
        1. Compare the key information points in both texts
        2. Check for any contradictions or incorrect information
        3. Consider semantic equivalence rather than exact wording
        4. Provide a single numerical score between 0 and 1

        Return only the numerical score without any explanation.
        """
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        score_text = response.text.strip()
        try:
            score = float(score_text)
            return max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
        except ValueError:
            st.error(f"Failed to parse correctness score: {score_text}")
            return 0.5  # Default middle score

    def evaluate_rag(self, question: str, answer: str, contexts: List[str], ground_truth: str = None) -> Dict[str, float]:
        """
        Comprehensive evaluation of a RAG system response
        """
        results = {
            "faithfulness": self.evaluate_faithfulness(answer, contexts),
            "relevance": self.evaluate_relevance(question, contexts),
            "contextual_precision": self.evaluate_contextual_precision(answer, question, contexts),
        }

        # Only evaluate correctness if ground truth is provided
        if ground_truth:
            results["answer_correctness"] = self.evaluate_answer_correctness(answer, ground_truth)

        # Calculate average score
        results["average_score"] = sum(results.values()) / len(results)

        return results