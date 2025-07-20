import os
import streamlit as st
from dotenv import load_dotenv
from utils.vector_store import load_vectorstore
from utils.vector_store import initialize_embeddings
from utils.llm_query import initialize_llm

# Load environment variables from .env file
load_dotenv()

# Import modular components
from utils.ui_components import apply_custom_css, render_vector_db_selector, render_search_interface, render_results_tab
from utils.search_operations import perform_search, generate_llm_answer

# Load configuration
#config = load_config()

INDEX_DIR = os.getenv("PATH_INDEX")
TOP_K = int(os.getenv("TOP_K", "30"))  # Default to 30 if not set
MODEL_LLM = os.getenv("MODEL_LLM")

# Streamlit page configuration
st.set_page_config(page_title="RAG Conscienciologia", page_icon="🔍", layout="wide")

# Apply custom CSS
apply_custom_css()

# Vector database options mapping
VECTOR_DB_OPTIONS = [
    ("700EXP", "VECTOR_STORE_ID_700EXP"),
    ("MANUAIS", "VECTOR_STORE_ID_MANUAIS"),
    ("CCG", "VECTOR_STORE_ID_CCG"),
    ("PROJ", "VECTOR_STORE_ID_PROJ"),
    ("HSR & HSP", "VECTOR_STORE_ID_HSRP"),
    ("ECWV", "VECTOR_STORE_ID_ECWV"),
    ("DAC", "VECTOR_STORE_ID_DAC"),
    ("LO", "VECTOR_STORE_ID_LO"),
    ("QUEST", "VECTOR_STORE_ID_QUEST"),
]

# Initialize embeddings
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = initialize_embeddings()

# Initialize LLM
if 'llm' not in st.session_state:
    st.session_state.llm = initialize_llm(model_name=MODEL_LLM, temperature=0)

# Ensure temperature is in session state
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.0

# Ensure top_k is in session state
if 'top_k' not in st.session_state:
    st.session_state.top_k = TOP_K

# Create column layout
col1, col2 = st.columns([1, 5])

# Left column - Vector Database selection and parameters
with col1:
    render_vector_db_selector(VECTOR_DB_OPTIONS)
    
    # Adicionar controles para temperature e TOP_K
    st.markdown("### Parâmetros de Busca")
    
    # Controle para TOP_K
    top_k_value = st.number_input(
        "TOP_K (número de resultados)", 
        min_value=1, 
        max_value=50, 
        value=TOP_K,
        step=1,
        help="Número de resultados a serem retornados pela busca"
    )
    st.session_state.top_k = top_k_value
    
    # Controle para temperature
    temperature_value = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.get('temperature', 0.0),
        step=0.1,
        help="Controla a aleatoriedade das respostas do LLM. Valores mais baixos são mais determinísticos."
    )
    st.session_state.temperature = temperature_value

# Right column - Main content
with col2:
    st.title("RAG Conscienciologia - Consulta de Documentos")
    
    # Search interface - returns both query and button state
    query, search_clicked = render_search_interface()
    
    # Handle search when button is clicked
    if search_clicked and query:
            # Get selected vector store IDs
            selected_vector_store_ids = st.session_state.get('vector_store_ids', [])
            
            # Ensure top_k is an integer
            top_k = int(st.session_state.top_k) if st.session_state.top_k is not None else 30
            
            # Perform search across selected vector stores
            all_results, grouped, sources_sorted = perform_search(
                query, 
                selected_vector_store_ids, 
                INDEX_DIR, 
                top_k
            )
            
            # Store results in session state
            if all_results:
                st.session_state.results = all_results
                st.session_state.query = query
                st.session_state.grouped = grouped
                st.session_state.sources_sorted = sources_sorted
                
                #LOG
                #st.write("All_results: ", all_results)
                st.write("Query: ",query)
                
                # Generate LLM answer
                answer = generate_llm_answer(query, all_results, st.session_state.llm, st.session_state.top_k, temperature=st.session_state.temperature)
                st.session_state.answer = answer

                st.write("Answer: ", answer)
                
                # Force page reload to show results
                st.rerun()

    # Display results if they exist in the session
    if 'results' in st.session_state and 'query' in st.session_state and 'answer' in st.session_state:
        # Create tabs for results
        tab1, tab2 = st.tabs(["Resposta LLM", "Resultados da Busca"])
        
        # Tab 1: LLM Answer
        with tab1:
            render_results_tab(
                st.session_state.query,
                st.session_state.answer,
                st.session_state.results,
                st.session_state.grouped,
                st.session_state.sources_sorted,
                show_documents=False,
                key_suffix="_llm_tab"
            )
        
        # Tab 2: Search Results
        with tab2:
            render_results_tab(
                st.session_state.query,
                st.session_state.answer,
                st.session_state.results,
                st.session_state.grouped,
                st.session_state.sources_sorted,
                show_llm_answer=False,
                key_suffix="_search_tab"
            )
       