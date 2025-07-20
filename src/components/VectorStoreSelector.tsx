import React from 'react';
import { Database } from 'lucide-react';
import { VectorStore } from '../types';

interface VectorStoreSelectorProps {
  stores: VectorStore[];
  selectedStores: string[];
  onStoreSelection: (storeId: string, checked: boolean) => void;
  onSelectAll: (checked: boolean) => void;
}

export const VectorStoreSelector: React.FC<VectorStoreSelectorProps> = ({
  stores,
  selectedStores,
  onStoreSelection,
  onSelectAll
}) => {
  const allSelected = stores.length > 0 && selectedStores.length === stores.length;

  return (
    <div className="vector-db-section">
      <h3><Database className="icon" /> Bases de Conhecimento</h3>
      <p className="subtitle">Selecione as bases de conhecimento para consulta</p>
      
      <div className="checkbox-group">
        {stores.length > 0 && (
          <>
            <label className="checkbox-item">
              <input
                type="checkbox"
                checked={allSelected}
                onChange={(e) => onSelectAll(e.target.checked)}
              />
              📚 Selecionar todos
            </label>
            <hr />
          </>
        )}
        
        {stores.map((store, index) => (
          <label key={store.id} className="checkbox-item">
            <input
              type="checkbox"
              checked={selectedStores.includes(store.id)}
              onChange={(e) => onStoreSelection(store.id, e.target.checked)}
            />
            {['📘', '📗', '📙'][index % 3]} {store.name}
          </label>
        ))}
        
        {stores.length === 0 && (
          <div className="status-indicator info">
            ℹ️ Faça upload de arquivos para criar bases de conhecimento
          </div>
        )}
        
        {stores.length > 0 && selectedStores.length > 0 && (
          <div className="status-indicator success">
            ✅ {selectedStores.length} base(s) selecionada(s)
          </div>
        )}
      </div>
    </div>
  );
};