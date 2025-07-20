import React, { useState, useEffect, useCallback } from 'react';
import { Search, Database, FileText, Download, Loader2, Brain, BookOpen } from 'lucide-react';
import OpenAI from 'openai';
import './App.css';

// Types
interface Document {
  id: string;
  content: string;
  metadata: {
    source: string;
    paragraph_number: number;
  };
  embedding?: number[];
}

interface SearchResult {
  document: Document;
  score: number;
}

interface VectorStore {
  id: string;
  name: string;
  documents: Document[];
}

interface GroupedResults {
  [source: string]: SearchResult[];
}

// Mock data representing the vector stores
const MOCK_VECTOR_STORES: VectorStore[] = [
  {
    id: '700exp',
    name: '700EXP',
    documents: [
      {
        id: '1',
        content: 'A Conscienciologia é a ciência que estuda a consciência de forma integral, abordando suas manifestações multidimensionais e evolutivas.',
        metadata: { source: '700 Experimentos da Conscienciologia', paragraph_number: 1 },
      },
      {
        id: '2',
        content: 'O paradigma consciencial propõe uma visão ampliada da realidade, considerando múltiplas dimensões de existência.',
        metadata: { source: '700 Experimentos da Conscienciologia', paragraph_number: 15 },
      },
    ]
  },
  {
    id: 'manuais',
    name: 'MANUAIS',
    documents: [
      {
        id: '3',
        content: 'A projeção consciente é o fenômeno pelo qual a consciência se manifesta fora do corpo físico de forma lúcida.',
        metadata: { source: 'Manual da Projeção Consciente', paragraph_number: 3 },
      },
      {
        id: '4',
        content: 'A bioenergética estuda as energias sutis que permeiam todos os seres vivos e suas interações.',
        metadata: { source: 'Manual de Bioenergética', paragraph_number: 7 },
      },
    ]
  },
  {
    id: 'dac',
    name: 'DAC',
    documents: [
      {
        id: '5',
        content: 'Autoconscientização: processo de desenvolvimento da lucidez sobre si mesmo, suas potencialidades e limitações.',
        metadata: { source: 'Dicionário de Argumentos da Conscienciologia', paragraph_number: 42 },
      },
      {
        id: '6',
        content: 'Cosmoética: conjunto de princípios morais universais aplicáveis a todas as dimensões de existência.',
        metadata: { source: 'Dicionário de Argumentos da Conscienciologia', paragraph_number: 156 },
      },
    ]
  }
];

// Utility functions
const cosineSimilarity = (a: number[], b: number[]): number => {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
};

const formatSourceName = (source: string): string => {
  return source
    .replace("Dicionário de Argumentos da Conscienciologia", "*Dicionário de Argumentos da Conscienciologia*")
    .replace("Manual da Projeção Consciente", "*Manual da Projeção Consciente*")
    .replace("Manual de Bioenergética", "*Manual de Bioenergética*");
};

// Simple text-based similarity for demo purposes
const calculateTextSimilarity = (query: string, text: string): number => {
  const queryWords = query.toLowerCase().split(/\s+/);
  const textWords = text.toLowerCase().split(/\s+/);
  
  let matches = 0;
  queryWords.forEach(word => {
    if (textWords.some(textWord => textWord.includes(word) || word.includes(textWord))) {
      matches++;
    }
  });
  
  return matches / queryWords.length;
};

const App: React.FC = () => {
  // State
  const [selectedStores, setSelectedStores] = useState<string[]>([]);
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [groupedResults, setGroupedResults] = useState<GroupedResults>({});
  const [llmAnswer, setLlmAnswer] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [isGeneratingAnswer, setIsGeneratingAnswer] = useState(false);
  const [topK, setTopK] = useState(10);
  const [temperature, setTemperature] = useState(0.0);
  const [activeTab, setActiveTab] = useState<'llm' | 'results'>('llm');
  const [openai, setOpenai] = useState<OpenAI | null>(null);

  // Initialize OpenAI
  useEffect(() => {
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
    if (apiKey) {
      setOpenai(new OpenAI({
        apiKey,
        dangerouslyAllowBrowser: true
      }));
    }
  }, []);

  // Handle vector store selection
  const handleStoreSelection = (storeId: string, checked: boolean) => {
    setSelectedStores(prev => 
      checked 
        ? [...prev, storeId]
        : prev.filter(id => id !== storeId)
    );
  };

  const handleSelectAll = (checked: boolean) => {
    setSelectedStores(checked ? MOCK_VECTOR_STORES.map(store => store.id) : []);
  };

  // Perform search
  const performSearch = useCallback(async () => {
    if (!query.trim() || selectedStores.length === 0) return;

    setIsSearching(true);
    setSearchResults([]);
    setGroupedResults({});
    setLlmAnswer('');

    try {
      // Get documents from selected stores
      const selectedDocuments = MOCK_VECTOR_STORES
        .filter(store => selectedStores.includes(store.id))
        .flatMap(store => store.documents);

      // Calculate similarity scores (using simple text similarity for demo)
      const results: SearchResult[] = selectedDocuments
        .map(doc => ({
          document: doc,
          score: calculateTextSimilarity(query, doc.content)
        }))
        .filter(result => result.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, topK);

      setSearchResults(results);

      // Group results by source
      const grouped: GroupedResults = {};
      results.forEach(result => {
        const source = formatSourceName(result.document.metadata.source);
        if (!grouped[source]) {
          grouped[source] = [];
        }
        grouped[source].push(result);
      });
      setGroupedResults(grouped);

      // Generate LLM answer if OpenAI is available
      if (openai && results.length > 0) {
        setIsGeneratingAnswer(true);
        await generateLLMAnswer(results);
      }

    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
      setIsGeneratingAnswer(false);
    }
  }, [query, selectedStores, topK, openai]);

  // Generate LLM answer
  const generateLLMAnswer = async (results: SearchResult[]) => {
    if (!openai) return;

    try {
      const context = results
        .slice(0, topK)
        .map(result => result.document.content)
        .join('\n\n');

      const response = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: 'Você é um assistente especializado em Conscienciologia que responde perguntas com base no contexto fornecido.'
          },
          {
            role: 'user',
            content: `Contexto:\n${context}\n\nPergunta: ${query}\nPor favor, responda com base apenas no contexto fornecido.`
          }
        ],
        temperature,
        max_tokens: 1000
      });

      setLlmAnswer(response.choices[0]?.message?.content || 'Não foi possível gerar uma resposta.');
    } catch (error) {
      console.error('LLM error:', error);
      setLlmAnswer('Erro ao gerar resposta com LLM. Verifique sua chave da API OpenAI.');
    }
  };

  // Export to DOCX (simplified - just download as text)
  const exportToDocx = () => {
    const content = `
RAG Conscienciologia - Resultados da Pesquisa

Pergunta: ${query}

Resposta LLM:
${llmAnswer}

Documentos Recuperados:
${searchResults.map((result, index) => `
${index + 1}. ${formatSourceName(result.document.metadata.source)} (Score: ${result.score.toFixed(4)})
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
  };

  return (
    <div className="app">
      <div className="container">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="vector-db-section">
            <h3><Database className="icon" /> Bases de Conhecimento</h3>
            <p className="subtitle">Selecione as bases de conhecimento para consulta</p>
            
            <div className="checkbox-group">
              <label className="checkbox-item">
                <input
                  type="checkbox"
                  checked={selectedStores.length === MOCK_VECTOR_STORES.length}
                  onChange={(e) => handleSelectAll(e.target.checked)}
                />
                📚 Selecionar todos
              </label>
              
              <hr />
              
              {MOCK_VECTOR_STORES.map((store, index) => (
                <label key={store.id} className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={selectedStores.includes(store.id)}
                    onChange={(e) => handleStoreSelection(store.id, e.target.checked)}
                  />
                  {['📘', '📗', '📙'][index % 3]} {store.name}
                </label>
              ))}
            </div>
            
            {selectedStores.length > 0 && (
              <div className="status-indicator success">
                ✅ {selectedStores.length} base(s) selecionada(s)
              </div>
            )}
            
            {selectedStores.length === 0 && (
              <div className="status-indicator info">
                ℹ️ Selecione pelo menos uma base de conhecimento
              </div>
            )}
          </div>

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
          
          {/* Search Interface */}
          <div className="search-container">
            <h3>Pesquisa de Documentos</h3>
            <p>Digite sua pergunta para buscar nos documentos selecionados</p>
            
            <div className="search-row">
              <input
                type="text"
                placeholder="Ex: O que é conscienciologia?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && performSearch()}
                className="search-input"
              />
              <button
                onClick={performSearch}
                disabled={isSearching || !query.trim() || selectedStores.length === 0}
                className="search-button"
              >
                {isSearching ? <Loader2 className="icon spinning" /> : <Search className="icon" />}
              </button>
            </div>
          </div>

          {/* Results */}
          {(searchResults.length > 0 || llmAnswer) && (
            <div className="results-section">
              {/* Tabs */}
              <div className="tabs">
                <button
                  className={`tab ${activeTab === 'llm' ? 'active' : ''}`}
                  onClick={() => setActiveTab('llm')}
                >
                  <Brain className="icon" /> Resposta LLM
                </button>
                <button
                  className={`tab ${activeTab === 'results' ? 'active' : ''}`}
                  onClick={() => setActiveTab('results')}
                >
                  <FileText className="icon" /> Resultados da Busca
                </button>
              </div>

              {/* Tab Content */}
              <div className="tab-content">
                {activeTab === 'llm' && (
                  <div className="llm-tab">
                    <div className="query-container">
                      <h3><Search className="icon" /> Pergunta</h3>
                      <p className="query-text">{query}</p>
                    </div>
                    
                    <div className="answer-container">
                      <h3><Brain className="icon" /> Resposta</h3>
                      {isGeneratingAnswer ? (
                        <div className="loading">
                          <Loader2 className="icon spinning" />
                          Gerando resposta...
                        </div>
                      ) : (
                        <div className="answer-text">{llmAnswer}</div>
                      )}
                    </div>
                  </div>
                )}

                {activeTab === 'results' && (
                  <div className="results-tab">
                    <div className="query-container">
                      <h3><Search className="icon" /> Pergunta</h3>
                      <p className="query-text">{query}</p>
                    </div>
                    
                    <h3><FileText className="icon" /> Top {topK} documentos por índice de similaridade</h3>
                    
                    {Object.entries(groupedResults).map(([source, results]) => (
                      <details key={source} className="source-group" open>
                        <summary>📚 {source}</summary>
                        <div className="source-content">
                          {results.map((result, index) => (
                            <div key={result.document.id} className="document-card">
                              <div className="document-header">
                                <span>Trecho {index + 1}</span>
                                <span className="score-badge">Score: {result.score.toFixed(4)}</span>
                              </div>
                              <div className="document-content">
                                {result.document.content}
                              </div>
                              <div className="document-metadata">
                                <BookOpen className="icon" />
                                Parágrafo: {result.document.metadata.paragraph_number}
                              </div>
                            </div>
                          ))}
                        </div>
                      </details>
                    ))}
                  </div>
                )}
              </div>

              {/* Export Button */}
              <div className="export-section">
                <button onClick={exportToDocx} className="export-button">
                  <Download className="icon" />
                  Exportar Resultados
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;