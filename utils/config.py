"""
Configuration settings for the RAG application.
"""
import os
from dotenv import load_dotenv

def load_config():
    """
    Load configuration from environment variables.
    
    Returns:
        dict: Configuration settings
    """
    # Load environment variables
    dotenv_path = os.getenv('DOTENV_PATH', '.env')
    load_dotenv(dotenv_path)
    
    # Define configuration
    config = {
        'TOP_K': 30,                              # número de documentos recuperados pelo ranking
        'MODEL_LLM': os.getenv("MODEL_LLM", "gpt-4o"),
    }
    
    # Add vector store IDs
    # Adicionar todas as variáveis VECTOR_STORE_ID_* do .env
    for key, value in os.environ.items():
        if key.startswith('VECTOR_STORE_ID_'):
            config[key] = value

    return config
