import React from 'react';
import { Search, Loader2 } from 'lucide-react';

interface SearchInterfaceProps {
  query: string;
  onQueryChange: (query: string) => void;
  onSearch: () => void;
  isSearching: boolean;
  disabled: boolean;
}

export const SearchInterface: React.FC<SearchInterfaceProps> = ({
  query,
  onQueryChange,
  onSearch,
  isSearching,
  disabled
}) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !disabled) {
      onSearch();
    }
  };

  return (
    <div className="search-container">
      <h3>Pesquisa de Documentos</h3>
      <p>Digite sua pergunta para buscar nos documentos selecionados</p>
      
      <div className="search-row">
        <input
          type="text"
          placeholder="Ex: O que é conscienciologia?"
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          onKeyPress={handleKeyPress}
          className="search-input"
        />
        <button
          onClick={onSearch}
          disabled={disabled || isSearching}
          className="search-button"
        >
          {isSearching ? (
            <Loader2 className="icon spinning" />
          ) : (
            <Search className="icon" />
          )}
        </button>
      </div>
    </div>
  );
};