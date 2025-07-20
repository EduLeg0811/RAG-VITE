"""
Session state management for the RAG application.
"""
import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.document_loader import load_markdown_documents
from utils.vector_store import initialize_embeddings
from utils.llm_query import initialize_llm

def initialize_session(config):
    """
    Initialize session state variables.
    
    Args:
        config (dict): Configuration dictionary
    """
    # Load documents if not already loaded
    if 'documents' not in st.session_state:
        with st.spinner("Carregando documentos..."):
            documents = load_markdown_documents(config['DATA_DIR'])
            
            if documents:
                st.session_state.documents = documents
            else:
                st.error(f"Diretório de dados não encontrado ou vazio: {config['DATA_DIR']}")
                st.session_state.documents = []
    
    # Apply chunking strategy
    if 'docs' not in st.session_state:
        if config['FLAG_PAR']:
            st.session_state.docs = st.session_state.documents
        else:
            # Use configured parameters for chunking
            chunk_size = config['CHUNK_SIZE']
            chunk_overlap = config['CHUNK_OVERLAP']
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            st.session_state.docs = splitter.split_documents(st.session_state.documents)
    
    # Initialize embeddings
    if 'embeddings' not in st.session_state:
        st.session_state.embeddings = initialize_embeddings()
    
    # Initialize LLM
    if 'llm' not in st.session_state:
        st.session_state.llm = initialize_llm(model_name=config['MODEL_LLM'], temperature=0)
    
    # Check for vector stores
    if 'vectorstore' not in st.session_state:
        verify_vector_stores(config['INDEX_DIR'])

def verify_vector_stores(index_dir):
    """
    Verify that vector stores exist.
    
    Args:
        index_dir (str): Directory containing vector stores
    """
    with st.spinner("🔄 Verificando índices vetoriais..."):
        # Check if index directory exists
        if not os.path.exists(index_dir):
            st.error(f"Diretório de índices não encontrado: {index_dir}")
            st.info("Execute 'streamlit run create_vector_store.py' para criar vector stores.")
            st.stop()
        
        # Check for user-created vector stores
        from utils.config import load_config
        config = load_config()
        vector_store_ids = [value for key, value in config.items() if key.startswith('VECTOR_STORE_ID_')]
        valid_stores = []
        
        for vector_id in vector_store_ids:
            index_path = os.path.join(index_dir, vector_id)
            index_file = os.path.join(index_path, "index.faiss")
            if os.path.exists(index_file):
                valid_stores.append(vector_id)
        
        if not valid_stores:
            st.error("Nenhum vector store válido encontrado.")
            st.info("Execute 'streamlit run create_vector_store.py' para criar vector stores.")
            st.stop()
            
        st.success(f"✅ {len(valid_stores)} vector stores encontrados e prontos para uso.")
        
        # Don't initialize any vectorstore by default
        # The vectorstore will be loaded only when the user selects one and makes a query
        st.session_state.vectorstore = None

def clear_search_results():
    """Clear session state variables related to search results."""
    keys_to_clear = [
        'query', 'results', 'answer', 'grouped', 'sources_sorted',
        'docx_generated', 'docx_success', 'docx_path', 'docx_data', 
        'docx_filename', 'docx_error'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
