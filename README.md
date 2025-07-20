# RAG Conscienciologia - Streamlit Application

![RAG Conscienciologia](https://img.shields.io/badge/RAG-Conscienciologia-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-red)
![OpenAI](https://img.shields.io/badge/OpenAI-1.82.1-green)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-orange)
![FAISS](https://img.shields.io/badge/FAISS-1.11.0-purple)

This is a Retrieval-Augmented Generation (RAG) application for Conscienciologia documents, built with Streamlit. The application combines semantic search with lexical search capabilities to provide comprehensive document retrieval and AI-powered responses based on the retrieved content.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Usage Guide](#usage-guide)
- [Vector Store Management](#vector-store-management)
- [Dropbox Integration](#dropbox-integration)
- [Document Processing](#document-processing)
- [Troubleshooting](#troubleshooting)

## Overview

The RAG Conscienciologia application is designed to search through specialized documents related to Conscienciologia, retrieve relevant information, and generate AI-powered responses based on the retrieved content. It combines both semantic search (using vector embeddings) and lexical search capabilities to provide comprehensive search results.

## Features

- **Multiple Vector Database Selection**: Choose from various knowledge bases to search through
- **Semantic Search**: Find relevant documents based on meaning rather than just keywords
- **Lexical Search**: Traditional keyword-based search for precise term matching
- **AI-Powered Responses**: Generate contextual answers using OpenAI's models
- **Document Generation**: Export search results to DOCX format
- **DOCX to Markdown Conversion**: Convert DOCX files to Markdown format for processing
- **Dropbox Integration**: Download and manage vector indices from Dropbox
- **Beautiful UI**: Modern, responsive interface with custom styling

## Project Structure

```
.
├── app.py                    # Main Streamlit application entry point
├── create_vector_store.py    # Script to create vector stores from documents
├── docx_converter_app.py     # Utility app to convert DOCX to Markdown
├── lexical_search.py         # Standalone lexical search functionality
├── OpenAI_Key.py            # OpenAI API key management
├── main.py                  # Alternative entry point
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── data/                    # Source document data
├── faiss_index/             # Vector database indexes
├── results/                 # Generated results and exports
├── converted_files/         # Converted Markdown files
└── utils/                   # Utility modules
    ├── __init__.py
    ├── config.py            # Configuration management
    ├── document_loader.py   # Document loading utilities
    ├── docx_converter.py    # DOCX to Markdown conversion
    ├── docx_generator.py    # Generate DOCX from search results
    ├── dropbox_manager.py   # Dropbox integration for index files
    ├── index_manager.py     # Vector index management
    ├── llm_query.py         # LLM query handling
    ├── search_operations.py # Search functionality
    ├── session_manager.py   # Streamlit session state management
    ├── ui_components.py     # UI components and styling
    ├── vector_store.py      # Vector store operations
    └── vector_store_creator.py # Vector store creation
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- Pandoc (for DOCX conversion)
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PATH_FILES=./data
   PATH_INDEX=./faiss_index
   PATH_RESULTS=./results
   MODEL_LLM=gpt-4o
   CHUNK_SIZE=500
   CHUNK_OVERLAP=50
   DROPBOX_ACCESS_TOKEN=your_dropbox_access_token
   VECTOR_STORE_ID_700EXP=700exp
   VECTOR_STORE_ID_MANUAIS=manuais
   VECTOR_STORE_ID_CCG=ccg
   VECTOR_STORE_ID_PROJ=proj
   VECTOR_STORE_ID_HSRP=hsrp
   VECTOR_STORE_ID_ECWV=ecwv
   VECTOR_STORE_ID_DAC=dac
   VECTOR_STORE_ID_LO=lo
   VECTOR_STORE_ID_QUEST=quest
   ```

## Running the Application

### Main RAG Application

```bash
streamlit run app.py
```

### DOCX Converter Utility

```bash
streamlit run docx_converter_app.py
```

### Lexical Search Utility

```bash
streamlit run lexical_search.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|--------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `PATH_FILES` | Directory for source documents | `./data` |
| `PATH_INDEX` | Directory for FAISS indexes | `./faiss_index` |
| `PATH_RESULTS` | Directory for generated results | `./results` |
| `MODEL_LLM` | OpenAI model to use | `gpt-4o` |
| `CHUNK_SIZE` | Size of text chunks for processing | `500` |
| `CHUNK_OVERLAP` | Overlap between text chunks | `50` |
| `DROPBOX_ACCESS_TOKEN` | Dropbox access token for index sync | Optional |
| `VECTOR_STORE_ID_*` | IDs for different vector stores | Required |

## Usage Guide

### Main RAG Application

1. **Select Knowledge Bases**: Choose which vector databases to include in your search
2. **Enter Query**: Type your search query in the search box
3. **View Results**: Results are displayed in three tabs:
   - **LLM Answer**: AI-generated response based on retrieved documents
   - **Search Results**: Raw search results grouped by source
   - **Generate DOCX**: Export results to a DOCX document

### DOCX Converter

1. **Upload DOCX**: Upload a DOCX file for conversion
2. **Convert**: Click the convert button to transform it to Markdown
3. **Save/Download**: Save the converted file to disk or download it

### Lexical Search

1. **Select Files**: Choose which Markdown files to search through
2. **Enter Search Term**: Type the exact term to search for
3. **View Results**: Results are displayed by file with highlighted search terms
4. **Export**: Generate a DOCX compilation of search results

## Vector Store Management

### Creating Vector Stores

To create new vector stores from documents:

```bash
python create_vector_store.py
```

This script processes documents in the `data` directory and creates FAISS indexes in the `faiss_index` directory.

### Managing Vector Stores

The application supports multiple vector stores, each defined by a `VECTOR_STORE_ID_*` environment variable. These IDs are used to organize and select different knowledge bases.

## Dropbox Integration

The application can download vector indices from Dropbox if they're not available locally. This is managed through the `dropbox_manager.py` module.

## Document Processing

### Document Loading

The application loads documents from Markdown files, processing them paragraph by paragraph. Each paragraph becomes a searchable document in the vector store.

### Document Generation

Search results can be exported to DOCX format with proper formatting and source attribution.

## Troubleshooting

### Missing Vector Indices

If vector indices are missing, the application will attempt to download them from Dropbox. If this fails, you'll need to create them using `create_vector_store.py`.

### OpenAI API Issues

If you encounter errors related to the OpenAI API, check your API key and ensure you have sufficient credits.

### Pandoc Errors

For DOCX conversion issues, ensure Pandoc is properly installed and accessible in your PATH.

---

🧠 Developed for Conscienciologia research and knowledge retrieval.
