export interface Document {
  id: string;
  content: string;
  metadata: {
    source: string;
    paragraph_number: number;
  };
  embedding?: number[];
}

export interface VectorStore {
  id: string;
  name: string;
  documents: Document[];
}

export interface SearchResult {
  document: Document;
  score: number;
}

export interface UploadedFile {
  id: string;
  name: string;
  content: string;
  processed: boolean;
}