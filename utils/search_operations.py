"""
Search operations for the RAG application.
"""
import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage
from utils.vector_store import load_vectorstore
from utils.vector_store import initialize_embeddings




def format_source_name(source):
    """
    Format source names for display.
    
    Args:
        source (str): Original source name
        
    Returns:
        str: Formatted source name
    """
    formatted = source.replace("12 - DAC (2014)", "*Dicionário de Argumentos da Conscienciologia*", 1)
    formatted = formatted.replace("13 - LO (2019) - II", "*Léxico de Ortopensatas*", 1)
    formatted = formatted.replace("13 - LO (2019) - I", "*Léxico de Ortopensatas*", 1)
    return formatted

def group_results_by_source(results):
    """
    Group search results by source.
    
    Args:
        results (list): List of (document, score) tuples
        
    Returns:
        dict: Dictionary with source as key and list of (document, score) as value
        list: Sorted list of source names
    """
    from collections import defaultdict
    
    # Agrupa resultados por fonte
    grouped = defaultdict(list)
    for doc, score in results:
        source = doc.metadata.get('source', '')
        fonte_display = format_source_name(source)
        grouped[fonte_display].append((doc, score))
    
    # Ordena as fontes alfabeticamente
    sources_sorted = sorted(grouped.keys())
    
    return grouped, sources_sorted



def perform_search(query, vector_store_ids, index_dir, top_k):
    """
    Perform search across multiple vector stores.
    
    Args:
        query (str): The search query
        vector_store_ids (list): List of vector store IDs to search
        index_dir (str): Directory containing vector stores
        top_k (int): Number of top results to return
        
    Returns:
        tuple: (all_results, grouped_results, sources_sorted)
    """
    # Check for valid vector store IDs
    missing_ids = [vid for vid in vector_store_ids if vid is None]
    valid_vector_store_ids = [vid for vid in vector_store_ids if vid is not None]
    
    if missing_ids:
        st.warning(f"Alguns Vector Store IDs não estão definidos no .env e serão ignorados: {missing_ids}")
    if not valid_vector_store_ids:
        st.warning("Nenhum Vector Store válido selecionado. Verifique seu .env.")
        return [], {}, []
    
    # Check if index directories exist
    missing_indices = []
    for vector_store_id in valid_vector_store_ids:
        index_path = os.path.join(index_dir, vector_store_id)
        if not os.path.exists(index_path):
            missing_indices.append(vector_store_id)
    
    if missing_indices:
        st.error(f"Os seguintes índices não foram encontrados: {', '.join(missing_indices)}")
        st.info("Execute 'create_vector_store.py' para criar os índices faltantes.")
        return [], {}, []
    
    # Search across all vector stores
    all_results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, vector_store_id in enumerate(valid_vector_store_ids):
        index_path = os.path.join(index_dir, vector_store_id)
        status_text.text(f"Pesquisando em {vector_store_id} ({i+1}/{len(valid_vector_store_ids)})")
        progress_bar.progress((i) / len(valid_vector_store_ids))
        
        try:
            with st.spinner(f"Buscando em {vector_store_id}..."):
                # Check if index file exists
                index_file = os.path.join(index_path, "index.faiss")
                if not os.path.exists(index_file):
                    st.warning(f"Arquivo de índice não encontrado para {vector_store_id}")
                    continue
                    
                # Load existing vector store
                try:
                    vectorstore = FAISS.load_local(
                        index_path,
                        st.session_state.embeddings,
                        allow_dangerous_deserialization=True
                    )
                    results = vectorstore.similarity_search_with_score(query, k=top_k)
                    all_results.extend(results)
                except Exception as e:
                    st.warning(f"Erro ao carregar vector store {vector_store_id}: {str(e)}")
        except Exception as e:
            st.warning(f"Não foi possível pesquisar no vector store {vector_store_id}: {e}")
    
    progress_bar.progress(1.0)
    status_text.text("Processando resultados...")
    
    # Sort all aggregated results by score (lower score = more similar)
    all_results = sorted(all_results, key=lambda x: x[1])
    # Limit to global top-k
    all_results = all_results[:top_k]
    
    # Group results by source
    grouped, sources_sorted = group_results_by_source(all_results)
    
    # Clear progress indicators
    status_text.empty()
    
    return all_results, grouped, sources_sorted

def generate_llm_answer(query, results, llm, top_k, temperature=0.2):
    """
    Generate LLM answer based on search results.
    
    Args:
        query (str): The search query
        results (list): List of (document, score) tuples
        llm: LLM object
        top_k (int): Number of documents to include in context
        temperature (float, optional): Controls randomness in LLM response generation. Defaults to 0.7.
        
    Returns:
        dict: Answer from the LLM
    """
    if not results:
        return {"result": "Nenhum resultado encontrado."}
    
    try:
        with st.spinner("Gerando resposta com LLM..."):
            # Build context from document texts
            context = "\n\n".join([doc.page_content for doc, _ in results[:top_k]])
            
            # Create messages for chat
            system_msg = "Você é um assistente especializado em Conscienciologia que responde perguntas com base no contexto fornecido."
            
            messages = [
                SystemMessage(content=system_msg),
                HumanMessage(content=f"Contexto:\n{context}\n\nPergunta: {query}\nPor favor, responda com base apenas no contexto fornecido.")
            ]
            
            # Invoke model with messages
            response = llm.invoke(messages, temperature=temperature)
            
            # Extract response content
            result_text = response.content if hasattr(response, 'content') else str(response)
            
            return {"result": result_text}
    except Exception as e:
        error_msg = f"Erro ao gerar resposta com LLM: {str(e)}"
        st.error(error_msg)
        return {"result": error_msg}
