
import streamlit as st
from typing import Tuple, Dict, Any
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import AIMessage, HumanMessage, Document
from langchain.schema.retriever import BaseRetriever
from langchain.schema.language_model import BaseLanguageModel

@st.cache_resource
def setup_rag_components() -> Tuple[BaseRetriever, Any]:
    """Initialize and cache RAG components."""
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    path = "pdf files"
    loader = PyPDFDirectoryLoader(path)
    extracted_docs = loader.load()
    splits = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = splits.split_documents(extracted_docs)
    vector_store = FAISS.from_documents(documents=docs, embedding=embedding)
    return vector_store.as_retriever(), docs

def create_rag_chain(llm: BaseLanguageModel, retriever: BaseRetriever, language: str) -> Dict[str, Any]:
    """Create RAG chains with different prompts for different types of questions."""
    # Alarm-related prompt
    alarm_prompt = ChatPromptTemplate.from_template(
        f"""
        You are a Telecom NOC Engineer with expertise in Radio Access Networks (RAN).
        Always respond in only {language} also always response should be in the structed format as mentioned.
        
        Previous conversation history:
        {{chat_history}}
        
        Current context: {{context}}
        Current question: {{input}}
        
        Response should be in short format and follow this structured format:
            1. Response: Provide an answer based on the given situation, with slight improvements for clarity but from the context.
            2. Explanation of the issue: Include a brief explanation on why the issue might have occurred.
            3. Recommended steps/actions: Suggest further steps to resolve the issue.
            4. Quality steps to follow:
                - Check for relevant INC/CRQ tickets.
                - Follow the TSDANC format while creating INC.
                - Mention previous closed INC/CRQ information if applicable.
                - If there are >= 4 INCs on the same issue within 90 days, highlight the ticket to the SAM-SICC team and provide all relevant details.
        """
    )
    
    # General conversation prompt
    general_prompt = ChatPromptTemplate.from_template(
        f"""
        You are a helpful NOC assistant.
        Always respond in {language}.
        
        Previous conversation history:
        {{chat_history}}
        
        Current context: {{context}}
        Current question: {{input}}
        
        Provide a natural, conversational response without following any specific format. 
        If the question is about chat history, give a brief and direct answer about previous interactions.
        Keep the response concise and relevant to the question asked.
        Please respond only if the question is related to history, context, telecom related, from knowledge base
        questions only. Don't answer questions which are not related to NOC Telecom operations.
        """
    )
    
    # Create chains
    alarm_chain = create_stuff_documents_chain(llm, alarm_prompt)
    general_chain = create_stuff_documents_chain(llm, general_prompt)
    
    return {
        'alarm': create_retrieval_chain(retriever, alarm_chain),
        'general': create_retrieval_chain(retriever, general_chain)
    }