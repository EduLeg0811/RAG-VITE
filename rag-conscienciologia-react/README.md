# RAG Conscienciologia - React Application

A React + TypeScript implementation of the RAG (Retrieval-Augmented Generation) Conscienciologia application, originally built in Python with Streamlit.

## Features

- **Vector Database Selection**: Choose from multiple knowledge bases (700EXP, MANUAIS, DAC, etc.)
- **Semantic Search**: Text-based similarity search through documents
- **AI-Powered Responses**: Generate contextual answers using OpenAI's GPT models
- **Modern UI**: Clean, responsive interface with glassmorphism design
- **Export Functionality**: Download search results as text files
- **Real-time Search**: Instant search with configurable parameters

## Setup

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```
   VITE_OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run Development Server**:
   ```bash
   npm run dev
   ```

## Architecture

### Key Components

- **App.tsx**: Main application component containing all functionality
- **Mock Vector Stores**: Simulated document databases with sample Conscienciologia content
- **Text Similarity**: Simple keyword-based similarity calculation for document ranking
- **OpenAI Integration**: GPT-4 integration for generating contextual responses

### Data Structure

```typescript
interface Document {
  id: string;
  content: string;
  metadata: {
    source: string;
    paragraph_number: number;
  };
}

interface VectorStore {
  id: string;
  name: string;
  documents: Document[];
}
```

### Search Algorithm

The application uses a simplified text-based similarity algorithm:

1. **Query Processing**: Split query into individual words
2. **Document Scoring**: Calculate similarity based on word matches
3. **Ranking**: Sort documents by similarity score
4. **Grouping**: Group results by source document
5. **LLM Generation**: Use top results as context for GPT-4 response

## Differences from Python Version

### Vector Store Implementation

- **Python Version**: Uses FAISS vector database with OpenAI embeddings
- **React Version**: Uses mock data with text-based similarity (for demo purposes)

### Real Vector Store Integration

To implement real vector stores in a production environment, you would need:

1. **Backend API**: Server-side endpoint to handle vector operations
2. **Embedding Service**: Generate embeddings for documents and queries
3. **Vector Database**: Use a browser-compatible solution like:
   - Weaviate with REST API
   - Pinecone with client SDK
   - Custom backend with FAISS/ChromaDB

### Suggested Production Architecture

```
Frontend (React) → Backend API → Vector Database
                              → OpenAI API
```

## Customization

### Adding Real Documents

Replace the `MOCK_VECTOR_STORES` array with real document data:

```typescript
const REAL_VECTOR_STORES: VectorStore[] = [
  {
    id: 'conscienciologia_docs',
    name: 'Conscienciologia Documents',
    documents: [
      // Load from your document collection
    ]
  }
];
```

### Implementing Real Vector Search

1. **Create Backend Endpoint**:
   ```typescript
   const searchDocuments = async (query: string, storeIds: string[]) => {
     const response = await fetch('/api/search', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ query, storeIds })
     });
     return response.json();
   };
   ```

2. **Update Search Function**:
   ```typescript
   const performSearch = async () => {
     const results = await searchDocuments(query, selectedStores);
     setSearchResults(results);
   };
   ```

## Technologies Used

- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **OpenAI SDK**: GPT integration
- **Lucide React**: Modern icon library
- **CSS3**: Custom styling with CSS variables

## Browser Compatibility

- Chrome/Edge 88+
- Firefox 78+
- Safari 14+

## Performance Considerations

- **Lazy Loading**: Implement for large document collections
- **Debounced Search**: Add search debouncing for better UX
- **Pagination**: Implement for large result sets
- **Caching**: Cache search results and embeddings

## Security Notes

- **API Key**: Never expose OpenAI API keys in production frontend
- **CORS**: Configure proper CORS policies for API endpoints
- **Rate Limiting**: Implement rate limiting for API calls

## Future Enhancements

1. **Real Vector Database Integration**
2. **Advanced Search Filters**
3. **Document Upload Interface**
4. **User Authentication**
5. **Search History**
6. **Bookmark Functionality**
7. **Advanced Export Options** (PDF, DOCX)
8. **Multi-language Support**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.