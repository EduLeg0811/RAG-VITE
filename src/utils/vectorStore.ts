import { Document, VectorStore, SearchResult } from '../types';
import { TextProcessor } from './textProcessor';

export class VectorStoreManager {
  private stores: Map<string, VectorStore> = new Map();

  createVectorStore(fileId: string, fileName: string, content: string): VectorStore {
    const documents = TextProcessor.createDocuments(content, fileName);
    
    const store: VectorStore = {
      id: fileId,
      name: fileName,
      documents
    };

    this.stores.set(fileId, store);
    return store;
  }

  getStore(id: string): VectorStore | undefined {
    return this.stores.get(id);
  }

  getAllStores(): VectorStore[] {
    return Array.from(this.stores.values());
  }

  search(query: string, storeIds: string[], topK: number = 10): SearchResult[] {
    const allResults: SearchResult[] = [];

    storeIds.forEach(storeId => {
      const store = this.stores.get(storeId);
      if (!store) return;

      store.documents.forEach(doc => {
        const score = TextProcessor.calculateTextSimilarity(query, doc.content);
        if (score > 0) {
          allResults.push({ document: doc, score });
        }
      });
    });

    return allResults
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  removeStore(id: string): void {
    this.stores.delete(id);
  }

  clear(): void {
    this.stores.clear();
  }
}