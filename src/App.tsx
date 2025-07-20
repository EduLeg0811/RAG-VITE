import React, { useState, useCallback, useMemo } from 'react';
import { FileUpload } from './components/FileUpload';
import { VectorStoreSelector } from './components/VectorStoreSelector';
import { SearchInterface } from './components/SearchInterface';
import { ResultsDisplay } from './components/ResultsDisplay';
import { VectorStoreManager } from './utils/vectorStore';
import { OpenAIService } from './utils/openai';
import { UploadedFile, SearchResult } from './types';
import './App.css';

const App: React.FC = () => {
  // Core state
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [selectedStores, setSelectedStores] = useState<string[]>([]);
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [llmAnswer, setLlmAnswer] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [isGeneratingAnswer, setIsGeneratingAnswer] = useState(false);
  const [activeTab, setActiveTab] = useState<'llm' | 'results'>('llm');
  
  // Parameters
  const [topK, setTopK] = useState(10);
  const [temperature, setTemperature] = useState(0.0);

  // Services
  const vectorStoreManager = useMemo(() => new VectorStoreManager(), []);
  const openaiService = useMemo(() => new OpenAIService(), []);

  // Get available vector stores
  const vectorStores = useMemo(() => vectorStoreManager.getAllStores(), [files]);

  // Handle file operations
  const handleFilesAdd = useCallback((newFiles: UploadedFile[]) => {
    setFiles(prev => [...prev, ...newFiles]);
    
    // Process files and create vector stores
    newFiles.forEach(file => {
      vectorStoreManager.createVectorStore(file.id, file.name, file.content);
      file.processed = true;
    });
  }, [vectorStoreManager]);

  const handleFileRemove = useCallback((fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
    vectorStoreManager.removeStore(fileId);
    setSelectedStores(prev => prev.filter(id => id !== fileId));
  }, [vectorStoreManager]);

  // Handle vector store selection
  const handleStoreSelection = useCallback((storeId: string, checked: boolean) => {
    setSelectedStores(prev => 
      checked 
        ? [...prev, storeId]
        : prev.filter(id => id !== storeId)
    );
  }, []);

  const handleSelectAll = useCallback((checked: boolean) => {
    setSelectedStores(checked ? vectorStores.map(store => store.id) : []);
  }, [vectorStores]);

  // Handle search
  const handleSearch = useCallback(async () => {
    if (!query.trim() || selectedStores.length === 0) return;

    setIsSearching(true);
    setSearchResults([]);
    setLlmAnswer('');

    try {
      // Perform search
      const results = vectorStoreManager.search(query, selectedStores, topK);
      setSearchResults(results);

      // Generate LLM answer if available and results exist
      if (openaiService.isAvailable() && results.length > 0) {
        setIsGeneratingAnswer(true);
        try {
          const answer = await openaiService.generateAnswer(query, results, temperature);
          setLlmAnswer(answer);
        } catch (error) {
          console.error('LLM error:', error);
          setLlmAnswer('Erro ao gerar resposta com LLM. Verifique sua chave da API OpenAI.');
        } finally {
          setIsGeneratingAnswer(false);
        }
      } else if (!openaiService.isAvailable()) {
        setLlmAnswer('Configure sua chave da API OpenAI para gerar respostas automáticas.');
      }

    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  }, [query, selectedStores, topK, temperature, vectorStoreManager, openaiService]);

  // Handle export
  const handleExport = useCallback(() => {
    const content = `
RAG Conscienciologia - Resultados da Pesquisa

Pergunta: ${query}

Resposta LLM:
${llmAnswer}

Documentos Recuperados:
${searchResults.map((result, index) => `
${index + 1}. ${result.document.metadata.source} (Score: ${result.score.toFixed(4)})
Parágrafo: ${result.document.metadata.paragraph_number}
Conteúdo: ${result.document.content}
`).join('\n')}
    `;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rag-results-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [query, llmAnswer, searchResults]);

  const canSearch = query.trim() && selectedStores.length > 0;
  const hasResults = searchResults.length > 0 || llmAnswer;

  return (
    <div className="app">
      <div className="container">
        {/* Sidebar */}
        <div className="sidebar">
          <FileUpload
            files={files}
            onFilesAdd={handleFilesAdd}
            onFileRemove={handleFileRemove}
          />
          
          <VectorStoreSelector
            stores={vectorStores}
            selectedStores={selectedStores}
            onStoreSelection={handleStoreSelection}
            onSelectAll={handleSelectAll}
          />

          <div className="parameters-section">
            <h3>Parâmetros de Busca</h3>
            
            <div className="parameter-item">
              <label>TOP_K (número de resultados)</label>
              <input
                type="number"
                min="1"
                max="50"
                value={topK}
                onChange={(e) => setTopK(parseInt(e.target.value))}
              />
            </div>
            
            <div className="parameter-item">
              <label>Temperature</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
              />
              <span className="parameter-value">{temperature.toFixed(1)}</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="main-content">
          <h1>RAG Conscienciologia - Consulta de Documentos</h1>
          
          <SearchInterface
            query={query}
            onQueryChange={setQuery}
            onSearch={handleSearch}
            isSearching={isSearching}
            disabled={!canSearch}
          />

          {hasResults && (
            <ResultsDisplay
              query={query}
              llmAnswer={llmAnswer}
              results={searchResults}
              activeTab={activeTab}
              onTabChange={setActiveTab}
              onExport={handleExport}
              isGeneratingAnswer={isGeneratingAnswer}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default App;