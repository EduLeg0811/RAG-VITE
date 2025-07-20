import React from 'react';
import { Search, Brain, FileText, BookOpen, Download } from 'lucide-react';
import { SearchResult } from '../types';

interface ResultsDisplayProps {
  query: string;
  llmAnswer: string;
  results: SearchResult[];
  activeTab: 'llm' | 'results';
  onTabChange: (tab: 'llm' | 'results') => void;
  onExport: () => void;
  isGeneratingAnswer: boolean;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({
  query,
  llmAnswer,
  results,
  activeTab,
  onTabChange,
  onExport,
  isGeneratingAnswer
}) => {
  const groupedResults = results.reduce((acc, result) => {
    const source = result.document.metadata.source;
    if (!acc[source]) acc[source] = [];
    acc[source].push(result);
    return acc;
  }, {} as Record<string, SearchResult[]>);

  return (
    <div className="results-section">
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'llm' ? 'active' : ''}`}
          onClick={() => onTabChange('llm')}
        >
          <Brain className="icon" /> Resposta LLM
        </button>
        <button
          className={`tab ${activeTab === 'results' ? 'active' : ''}`}
          onClick={() => onTabChange('results')}
        >
          <FileText className="icon" /> Resultados da Busca
        </button>
      </div>

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
                  <Brain className="icon spinning" />
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
            
            <h3><FileText className="icon" /> Documentos encontrados</h3>
            
            {Object.entries(groupedResults).map(([source, sourceResults]) => (
              <details key={source} className="source-group" open>
                <summary>📚 {source}</summary>
                <div className="source-content">
                  {sourceResults.map((result, index) => (
                    <div key={result.document.id} className="document-card">
                      <div className="document-header">
                        <span>Parágrafo {result.document.metadata.paragraph_number}</span>
                        <span className="score-badge">
                          Score: {result.score.toFixed(4)}
                        </span>
                      </div>
                      <div className="document-content">
                        {result.document.content}
                      </div>
                    </div>
                  ))}
                </div>
              </details>
            ))}
          </div>
        )}
      </div>

      <div className="export-section">
        <button onClick={onExport} className="export-button">
          <Download className="icon" />
          Exportar Resultados
        </button>
      </div>
    </div>
  );
};