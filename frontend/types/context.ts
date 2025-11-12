/**
 * コンテキスト取得関連の型定義
 */

export type SourceType = 'notion' | 'slack' | 'atlassian';

export interface ContextItem {
  source: SourceType;
  title: string;
  content: string;
  url: string | null;
  metadata: {
    section?: string;
    [key: string]: any;
  } | null;
}

export interface ContextRetrievalRequest {
  topic: string;
  keywords?: string[];
}

export interface ContextRetrievalResponse {
  topic: string;
  keywords: string[];
  count: number;
  contexts: ContextItem[];
}

export interface SourceInfo {
  name: string;
  enabled: boolean;
  description: string;
}

export interface SourcesResponse {
  sources: SourceInfo[];
  dedalus_configured: boolean;
  context_retrieval_enabled: boolean;
}
