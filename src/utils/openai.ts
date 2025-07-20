import OpenAI from 'openai';
import { SearchResult } from '../types';

export class OpenAIService {
  private client: OpenAI | null = null;

  constructor() {
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
    if (apiKey) {
      this.client = new OpenAI({
        apiKey,
        dangerouslyAllowBrowser: true
      });
    }
  }

  isAvailable(): boolean {
    return this.client !== null;
  }

  async generateAnswer(
    query: string, 
    results: SearchResult[], 
    temperature: number = 0.0
  ): Promise<string> {
    if (!this.client) {
      throw new Error('OpenAI client not initialized');
    }

    const context = results
      .map(result => result.document.content)
      .join('\n\n');

    const response = await this.client.chat.completions.create({
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

    return response.choices[0]?.message?.content || 'Não foi possível gerar uma resposta.';
  }
}