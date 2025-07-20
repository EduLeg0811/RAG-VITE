"""
LLM query handling for the RAG application.
"""
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os

def initialize_llm(model_name="gpt-4.1-nano-2025-04-14", temperature=0):
    """
    Initialize LLM for query answering.
    
    Args:
        model_name (str): Name of the OpenAI model to use
        temperature (float): Temperature parameter for the model
        
    Returns:
        ChatOpenAI: LLM object
    """
    return ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=os.getenv("OPENAI_API_KEY"))

def query_llm(query, vectorstore, llm, top_k=30):
    """
    Query the LLM using RetrievalQA.
    
    Args:
        query (str): The query string
        vectorstore: Vector store object
        llm: LLM object
        top_k (int): Number of documents to retrieve
        
    Returns:
        dict: Answer from the LLM
        list: List of (document, score) tuples
    """
    # Get similar documents
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    
    # Query LLM
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": top_k}),
        return_source_documents=True
    )
    answer = qa.invoke({"query": query})
    
    return answer, results
