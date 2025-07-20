"""
Vector store operations for the RAG application.
"""
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def initialize_embeddings():
    """
    Initialize OpenAI embeddings.
    
    Returns:
        OpenAIEmbeddings: Embeddings object
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAIEmbeddings(openai_api_key=api_key)

def load_vectorstore(docs, embeddings, index_dir):
    """
    Load existing vector store or create a new one if force_rebuild is True.
    This function should only be used by create_vector_store.py for creating new indices.
    The app.py should only load existing indices.
    
    Args:
        docs (list): List of Document objects
        embeddings: Embeddings object
        index_dir (str): Directory to save/load the index
        force_rebuild (bool): Force rebuilding the index
        
    Returns:
        tuple: (FAISS vector store object, status string)
    """
    # Verificar se o arquivo de índice realmente existe
    index_file = os.path.join(index_dir, "index.faiss")
    
    # Se o arquivo existe e não estamos forçando recriação, carregue-o
    if os.path.exists(index_file):
        try:
            # Load existing index
            vectorstore = FAISS.load_local(
                index_dir,
                embeddings,
                allow_dangerous_deserialization=True
            )
            return vectorstore, "loaded"
        except Exception as e:
            raise Exception(f"Erro ao carregar índice existente: {e}")
    
   
