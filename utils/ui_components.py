"""
UI components for the RAG application.
"""
import os
import subprocess
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app."""
    # Import Google Font
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)
    
    # CSS Variables and Theme
    st.markdown("""
    <style>
    :root {
        /* Color Palette */
        --color-bg: #f8f9fa;
        --color-bg-dark: #1e1e2e;
        --color-text: #333333;
        --color-text-dark: #e0e0e0;
        --color-primary: #4361ee;
        --color-primary-dark: #3a56d4;
        --color-secondary: #3a0ca3;
        --color-accent: #4cc9f0;
        --color-accent-light: #80e9ff;
        --color-success: #2ec4b6;
        --color-warning: #ff9f1c;
        --color-error: #e71d36;
        
        /* Glassmorphism */
        --glass-bg: rgba(255, 255, 255, 0.7);
        --glass-bg-dark: rgba(30, 30, 46, 0.7);
        --glass-border: rgba(255, 255, 255, 0.2);
        --glass-border-dark: rgba(255, 255, 255, 0.1);
        
        /* Shadows */
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
        
        /* Rounded corners */
        --radius-sm: 0.25rem;
        --radius-md: 0.5rem;
        --radius-lg: 1rem;
        --radius-full: 50%;
    }
    
    /* Base Styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--color-bg);
        color: var(--color-text);
    }
    
    /* Prevent hover effects on the entire page */
    html, body, div, span, button, a, input, textarea, select, label, *, *::before, *::after {
        transition: none !important;
        transform: none !important;
    }
    
    *:hover {
        background-color: inherit !important;
        transform: none !important;
        box-shadow: inherit !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--color-secondary);
        margin-bottom: 1.5rem;
    }
    
    h2 {
        font-size: 1.5rem;
        color: var(--color-primary);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.25rem;
        color: var(--color-secondary);
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    p {
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    /* Layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 1.5rem;
    }
    
    div[data-testid="stHorizontalBlock"] {
        gap: 1.5rem;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background-color: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    /* Vector DB Selection */
    .vector-db-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        color: var(--color-secondary);
    }
    
    .stCheckbox label {
        font-weight: 500;
        display: flex;
        align-items: center;
    }
    
    .vector-db-container {
        background: var(--glass-bg);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    /* Buttons */
    .stButton button {
        border-radius: var(--radius-md);
        font-weight: 600;
        padding: 0.5rem 1.25rem;
        border: none;
        background-color: var(--color-primary);
        color: white;
        box-shadow: var(--shadow-sm);
    }
    
    .stButton button:hover {
        background-color: var(--color-primary-dark);
    }
    
    /* Round Action Buttons */
    .action-button {
        border-radius: var(--radius-full);
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--color-primary);
        color: white;
        box-shadow: var(--shadow-md);
        border: none;
        cursor: pointer;
    }
    
    .action-button:hover {
        background-color: var(--color-primary-dark);
    }
    
    /* Search Input */
    .stTextInput input {
        border-radius: var(--radius-md);
        border: 1px solid var(--glass-border);
        padding: 0.75rem 1rem;
        background-color: var(--glass-bg);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: var(--shadow-sm);
    }
    
    .stTextInput input:focus {
        border-color: var(--color-primary);
        box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: var(--glass-bg);
        border-radius: var(--radius-md);
        padding: 0.5rem;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid var(--glass-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-md);
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--color-primary);
        color: white;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--color-secondary);
        background-color: var(--glass-bg);
        border-radius: var(--radius-md);
        padding: 0.75rem 1rem;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }
    
    .streamlit-expanderContent {
        border: 1px solid var(--glass-border);
        border-top: none;
        border-radius: 0 0 var(--radius-md) var(--radius-md);
        padding: 1rem;
        background-color: rgba(255, 255, 255, 0.5);
    }
    
    /* Info/Warning/Error Boxes */
    .stAlert {
        background-color: var(--glass-bg);
        border-radius: var(--radius-md);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-sm);
    }
    
    .stAlert [data-baseweb="notification"] {
        border-radius: var(--radius-md);
        width: 100%;
    }
    
    /* Dividers */
    hr {
        margin: 1.5rem 0;
        opacity: 0.2;
    }
    
    /* Spinner */
    .stSpinner {
        text-align: center;
        padding: 2rem 0;
    }
    
    /* Download Button */
    .download-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background-color: var(--color-success);
        color: white;
        border-radius: var(--radius-md);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        box-shadow: var(--shadow-sm);
    }
    
    .download-button:hover {
        background-color: #25a99d;
    }
    
    /* Code Blocks */
    code {
        font-family: 'SF Mono', 'Consolas', 'Monaco', 'Andale Mono', monospace;
        background-color: rgba(0, 0, 0, 0.05);
        padding: 0.2em 0.4em;
        border-radius: var(--radius-sm);
        font-size: 0.9em;
    }
    
    pre {
        background-color: var(--color-bg-dark);
        color: var(--color-text-dark);
        padding: 1rem;
        border-radius: var(--radius-md);
        overflow-x: auto;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.75rem;
        }
        
        h2 {
            font-size: 1.35rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add custom icons and components
    st.markdown("""
    <style>
    /* Custom icon classes */
    .icon-search::before {
        font-family: "Font Awesome 6 Free";
        content: "\f002";
        font-weight: 900;
        margin-right: 0.5rem;
    }
    
    .icon-document::before {
        font-family: "Font Awesome 6 Free";
        content: "\f15c";
        font-weight: 900;
        margin-right: 0.5rem;
    }
    
    .icon-download::before {
        font-family: "Font Awesome 6 Free";
        content: "\f019";
        font-weight: 900;
        margin-right: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_vector_db_selector(vector_db_options):
    """
    Render the vector database selector UI.
    
    Args:
        vector_db_options (list): List of (label, env_key) tuples
        
    Returns:
        list: List of selected vector store IDs
    """
    import os
    # Header with icon
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3><i class="fas fa-database" style="color: var(--color-primary);"></i> Bases de Conhecimento</h3>
        <p style="font-size: 0.9rem; opacity: 0.8;">Selecione as bases de conhecimento para consulta</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Extract labels and create ID map using environment variables directly
    vector_db_labels = [label for label, _ in vector_db_options]
    vector_db_id_map = {label: os.getenv(env_key) for label, env_key in vector_db_options}
    
    # Glassmorphism container for the selector
    with stylable_container(
        key="vector-db-container",
        css_styles="""{
            background-color: var(--glass-bg);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }"""
    ):
        # Select all option with custom styling
        col1, col2 = st.columns([3, 1])
        with col1:
            select_all = st.checkbox(
                "📚 Selecionar todos", 
                key="select_all_checkbox",
                help="Seleciona todas as bases de conhecimento disponíveis"
            )
        
        st.markdown("<hr style='margin: 0.75rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        
        # Individual checkboxes with icons and hover effects
        selected_labels = []
        for i, label in enumerate(vector_db_labels):
            # Add custom icon based on database type
            icon = "📘" if i % 3 == 0 else "📗" if i % 3 == 1 else "📙"
            
            # Create a stylable container for each checkbox for hover effect
            with stylable_container(
                key=f"db_item_{i}",
                css_styles="""{
                    padding: 0rem;
                    border-radius: var(--radius-sm);
                }"""
            ):
                is_checked = st.checkbox(
                    f"{icon} {label}", 
                    value=select_all, 
                    key=f"checkbox_{label}"
                )
                if is_checked:
                    selected_labels.append(label)
        
        # Map to IDs and filter out None values
        selected_vector_store_ids = [vector_db_id_map[label] for label in selected_labels if label in vector_db_id_map]
        valid_vector_store_ids = [vid for vid in selected_vector_store_ids if vid is not None]
        
        # Show status indicator
        if valid_vector_store_ids:
            st.write("")
            st.success(f"✅ {len(valid_vector_store_ids)} base(s) selecionada(s)")
        else:
            st.write("")
            st.info("ℹ️ Selecione pelo menos uma base de conhecimento")
        
        # Show warning for missing IDs with improved styling
        missing_labels = [label for label in selected_labels if vector_db_id_map.get(label) is None]
        if missing_labels:
            with stylable_container(
                key="missing_ids_warning",
                css_styles="""{
                    background-color: rgba(255, 159, 28, 0.1);
                    border-left: 4px solid var(--color-warning);
                    padding: 0.5rem 1rem;
                    border-radius: var(--radius-sm);
                    margin-top: 0.5rem;
                }"""
            ):
                st.warning(f"⚠️ As seguintes opções não possuem ID definido no .env e serão ignoradas: {', '.join(missing_labels)}")
    
    # Store in session state
    st.session_state['vector_store_ids'] = valid_vector_store_ids
    
    return valid_vector_store_ids

def render_search_interface():
    """
    Render a clean, modern search interface.
    
    Returns:
        tuple: A tuple containing (query, search_clicked)
            - query (str): The search query
            - search_clicked (bool): Whether the search button was clicked
    """
    # Main container with clean styling
    with stylable_container(
        key="search_container",
        css_styles="""{
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #e9ecef;
        }"""
    ):
        # Search header
        st.markdown("""
        <div style="margin-bottom: 1.25rem;">
            <h3 style="margin: 0 0 0.5rem 0; color: #2c3e50;">Pesquisa de Documentos</h3>
            <p style="margin: 0; color: #6c757d; font-size: 0.95rem;">
                Digite sua pergunta para buscar nos documentos selecionados
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Search row with input and button
        col1, col2 = st.columns([5, 1])
        
        with col1:
            # Custom input styling
            st.markdown("""
            <style>
                .stTextInput>div>div>input {
                    height: 48px;
                    border-radius: 24px 0 0 24px !important;
                    border: 1px solid #e0e0e0;
                    padding: 0 20px;
                    font-size: 1rem;
                    transition: all 0.2s;
                    box-shadow: none;
                }
                .stTextInput>div>div>input:focus {
                    border-color: #4a6cf7;
                    box-shadow: 0 0 0 2px rgba(74, 108, 247, 0.2);
                }
                .stTextInput>div>div>input::placeholder {
                    color: #adb5bd;
                }
            </style>
            """, unsafe_allow_html=True)
            
            query = st.text_input(
                "Digite sua pergunta:",
                key="search_query",
                placeholder="Ex: O que é conscienciologia?",
                label_visibility="collapsed"
            )
        
        with col2:
            # Button styling
            st.markdown("""
            <style>
                .stButton>button {
                    height: 48px !important;
                    min-width: 48px !important;
                    border-radius: 0 24px 24px 0 !important;
                    background: linear-gradient(135deg, #4a6cf7 0%, #3a56d5 100%);
                    border: none;
                    color: white;
                    font-size: 1.2rem;
                    padding: 0;
                    margin: 0;
                    transition: all 0.2s;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 4px rgba(74, 108, 247, 0.2);
                }
                .stButton>button:hover {
                    background: linear-gradient(135deg, #3a56d5 0%, #2c42b4 100%);
                    transform: translateY(-1px);
                    box-shadow: 0 4px 8px rgba(74, 108, 247, 0.3);
                }
                .stButton>button:active {
                    transform: translateY(0);
                    box-shadow: 0 2px 4px rgba(74, 108, 247, 0.2);
                }
            </style>
            """, unsafe_allow_html=True)
            
            search_clicked = st.button(
                "🔍",
                key="search_button",
                use_container_width=True
            )
    
    return query, search_clicked

def render_results_tab(query, answer, results, grouped=None, sources_sorted=None, top_k=10, show_llm_answer=True, show_documents=True, key_suffix=""):
    """
    Render the results tab with LLM answer and retrieved documents.
    
    Args:
        query (str): The search query
        answer (dict or str): The LLM answer
        results (list): List of (document, score) tuples
        grouped (dict, optional): Results grouped by source
        sources_sorted (list, optional): Sorted list of sources
        top_k (int): Number of top results to display
        show_llm_answer (bool): Whether to show the LLM answer
        show_documents (bool): Whether to show the retrieved documents
        key_suffix (str): Suffix to add to keys to avoid duplicates
    """
    # Display query in a styled container
    with stylable_container(
        key=f"query_container{key_suffix}",
        css_styles="""{
            background-color: var(--glass-bg);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--glass-border);
            border-left: 4px solid var(--color-primary);
        }"""
    ):
        st.markdown(f"""<h3 style="margin-top: 0;"><i class="fas fa-question-circle" style="color: var(--color-primary);"></i> Pergunta</h3>
        <p style="font-size: 1.1rem; font-weight: 500;">{query}</p>""", unsafe_allow_html=True)
    
    # Display answer only if show_llm_answer is True
    if show_llm_answer:
        with stylable_container(
            key=f"answer_container{key_suffix}",
            css_styles="""{
                background-color: var(--glass-bg);
                border-radius: var(--radius-md);
                padding: 1.25rem;
                margin-bottom: 1.5rem;
                box-shadow: var(--shadow-sm);
                border: 1px solid var(--glass-border);
                border-left: 4px solid var(--color-secondary);
            }"""
        ):
            # Handle different answer formats (dict or string)
            answer_text = answer["result"] if isinstance(answer, dict) and "result" in answer else answer
            st.markdown(f"""<h3 style="margin-top: 0;"><i class="fas fa-robot" style="color: var(--color-secondary);"></i> Resposta</h3>
            <div style="line-height: 1.6;">{answer_text}</div>""", unsafe_allow_html=True)
    
    # Display retrieved documents only if show_documents is True
    if show_documents:
        # Display retrieved documents header
        st.markdown(f"""<h3><i class="fas fa-file-alt" style="color: var(--color-primary);"></i> Top {top_k} documentos por índice de similaridade</h3>""", unsafe_allow_html=True)
        
        # If we have grouped results, display them by source with improved styling
        if grouped and sources_sorted:
            for source_idx, source in enumerate(sources_sorted):
                formatted_source = format_source_name(source)
                
                # Create a styled expander for each source
                with stylable_container(
                    key=f"source_container_{source_idx}{key_suffix}",
                    css_styles="""{
                        margin-bottom: 1rem;
                    }"""
                ):
                    with st.expander(f"📚 {formatted_source}"):
                        for doc_idx, (doc, score) in enumerate(grouped[source]):
                            # Create a card for each document
                            with stylable_container(
                                key=f"doc_card_{source_idx}_{doc_idx}{key_suffix}",
                                css_styles="""{
                                    background-color: rgba(255, 255, 255, 0.5);
                                    border-radius: var(--radius-md);
                                    padding: 0.5rem;
                                    margin-bottom: 1rem;
                                    border: 1px solid var(--glass-border);
                                }"""
                            ):
                                # Score badge
                                # st.markdown(f"""<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                #     <span style="font-weight: 600; color: var(--color-text);">Trecho {doc_idx+1}</span>
                                #     <span style="background-color: var(--color-primary); color: white; padding: 0.2rem 0.5rem; border-radius: var(--radius-sm); font-size: 0.8rem; font-weight: 600;">
                                #         Score: {score:.4f}
                                #     </span>
                                # </div>""", unsafe_allow_html=True)
                                
                                # Document content with markdown rendering
                                with st.container():
                                                                       
                                    # Metadata
                                    paragraph_num = doc.metadata.get('paragraph_number', 'N/A')
                                    st.markdown(f"""
                                    <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 0rem;">
                                        <i class="fas fa-paragraph"></i> Parágrafo: {paragraph_num}  -  Score: {score:.4f}
                                    </div>
                                    """, unsafe_allow_html=True)
                                    #st.markdown("---")

                                    st.markdown(doc.page_content, unsafe_allow_html=False)


        # Otherwise, display flat results with improved styling
        else:
            # Limit to top_k results for better visualization
            for i, (doc, score) in enumerate(results[:top_k]):
                m = doc.metadata
                snippet = doc.page_content.replace("\n", " ").strip()
                source_name = format_source_name(m['source'])
                
                # Create a styled expander for each result
                with stylable_container(
                    key=f"result_container_{i}{key_suffix}",
                    css_styles="""{
                        margin-bottom: 0.25rem;
                    }"""
                ):
                    with st.expander(f"{i+1}. {source_name} (Score: {score:.4f})"):
                        # Create a card for the document
                        with stylable_container(
                            key=f"flat_doc_card_{i}{key_suffix}",
                            css_styles="""{
                                background-color: rgba(255, 255, 255, 0.5);
                                border-radius: var(--radius-md);
                                padding: 0.5rem;
                                margin-bottom: 0.5rem;
                                border: 1px solid var(--glass-border);
                            }"""
                        ):
                            # Document content with markdown rendering
                            with st.container():
                                #st.markdown("---")
                                st.markdown(snippet, unsafe_allow_html=False)
                                
                                # Metadata
                                paragraph_num = m.get('paragraph_number', 'N/A')
                                st.markdown(f"""
                                <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 0rem; display: flex; gap: 0rem;">
                                    <span><i class="fas fa-book"></i> {source_name}</span>
                                    <span><i class="fas fa-paragraph"></i> Parágrafo: {paragraph_num}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                #st.markdown("---")


def format_source_name(source):
    """Format source name for display."""
    formatted = source.replace("12 - DAC (2014)", "*Dicionário de Argumentos da Conscienciologia*", 1)
    formatted = formatted.replace("13 - LO (2019) - II", "*Léxico de Ortopensatas*", 1)
    formatted = formatted.replace("13 - LO (2019) - I", "*Léxico de Ortopensatas*", 1)
    return formatted

def render_docx_tab(query, answer, grouped_results, sources_sorted, results_dir):
    """
    Render the DOCX generation tab.
    
    Args:
        query (str): The search query
        answer (dict or str): The LLM answer
        grouped_results (dict): Results grouped by source
        sources_sorted (list): Sorted list of sources
        results_dir (str): Directory to save results
        
    Returns:
        bool: Whether to generate DOCX
    """
    from utils.docx_generator import generate_docx_from_results
    import os
    import subprocess
    
    # Header with icon
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3><i class="fas fa-file-word" style="color: var(--color-primary);"></i> Exportar para DOCX</h3>
        <p style="font-size: 0.9rem; opacity: 0.8;">Gere um documento Word formatado com os resultados da sua pesquisa</p>
    </div>
    """, unsafe_allow_html=True)

    # Botão para iniciar nova consulta
    if st.button("🔍 Nova Consulta", key="new_query", use_container_width=True):
        # Clear session state for a new query
        clear_session_state()
        # Reload page
        st.rerun()
       
     

def clear_session_state():
    """Clear session state variables related to search results."""
    keys_to_clear = [
        'query', 'results', 'answer', 'grouped', 
        'docx_generated', 'docx_success'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
