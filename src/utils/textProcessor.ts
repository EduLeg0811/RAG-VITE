import { Document } from '../types';

export class TextProcessor {
  static splitIntoParagraphs(text: string): string[] {
    return text
      .split(/\n\s*\n/) // Split on double newlines
      .map(paragraph => paragraph.trim())
      .filter(paragraph => paragraph.length > 0);
  }

  static createDocuments(content: string, source: string): Document[] {
    const paragraphs = this.splitIntoParagraphs(content);
    
    return paragraphs.map((paragraph, index) => ({
      id: `${source}_${index + 1}`,
      content: paragraph,
      metadata: {
        source,
        paragraph_number: index + 1
      }
    }));
  }

  static calculateTextSimilarity(query: string, text: string): number {
    const queryWords = query.toLowerCase().split(/\s+/);
    const textWords = text.toLowerCase().split(/\s+/);
    
    let matches = 0;
    queryWords.forEach(word => {
      if (textWords.some(textWord => 
        textWord.includes(word) || word.includes(textWord)
      )) {
        matches++;
      }
    });
    
    return matches / queryWords.length;
  }
}