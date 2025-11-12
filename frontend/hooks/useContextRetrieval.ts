/**
 * コンテキスト取得カスタムフック
 */
'use client';

import { useState } from 'react';
import { ContextItem, ContextRetrievalResponse } from '@/types/context';

// モックデータ
const MOCK_CONTEXTS: ContextItem[] = [
  {
    source: 'notion',
    title: 'プロダクト開発ロードマップ 2024',
    content: '過去3ヶ月のスプリントで、ユーザー認証機能、検索機能、通知システムの3つの主要機能を実装しました。次の四半期では、パフォーマンス最適化とモバイル対応に注力する予定です。',
    url: 'https://notion.so/product-roadmap-2024',
    metadata: {
      section: 'Product Strategy',
      lastUpdated: '2024-01-15'
    }
  },
  {
    source: 'slack',
    title: '#engineering チャンネル - 新機能のデプロイについて',
    content: '@tanaka: 新機能のデプロイスケジュールについて、来週月曜日の午前10時を予定しています。事前にステージング環境での確認をお願いします。\n@suzuki: 了解しました。金曜日までにQAを完了させます。',
    url: null,
    metadata: {
      channel: '#engineering',
      timestamp: '2024-01-18T14:30:00Z'
    }
  },
  {
    source: 'atlassian',
    title: 'PROJ-123: ユーザー検索機能の実装',
    content: 'ステータス: 進行中\n担当者: 田中太郎\n\n概要: ユーザー名、メールアドレス、タグによる高度な検索機能を実装します。Elasticsearchを使用し、リアルタイム検索を実現します。',
    url: 'https://jira.example.com/browse/PROJ-123',
    metadata: {
      status: 'In Progress',
      assignee: '田中太郎',
      priority: 'High'
    }
  },
  {
    source: 'notion',
    title: 'ユーザーフィードバック集約 - 2024年1月',
    content: '今月のユーザーフィードバックでは、検索機能の改善要望が最も多く寄せられています。特に、フィルター機能の追加と検索速度の向上が求められています。',
    url: 'https://notion.so/user-feedback-jan-2024',
    metadata: {
      section: 'User Research'
    }
  },
  {
    source: 'slack',
    title: '#design チャンネル - UI改善提案',
    content: '@design-lead: 検索結果画面のUIについて、カード形式よりリスト形式の方が情報密度が高く、スキャンしやすいという意見があります。A/Bテストを実施しましょう。',
    url: null,
    metadata: {
      channel: '#design'
    }
  }
];

export function useContextRetrieval() {
  const [contexts, setContexts] = useState<ContextItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const retrieveContext = async (topic: string, keywords?: string[]) => {
    setLoading(true);
    setError(null);

    try {
      // モック: 1.5秒の遅延をシミュレート
      await new Promise((resolve) => setTimeout(resolve, 1500));

      // 実際のAPIコール（将来の実装用）
      // const response = await fetch('/api/context/retrieve', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ topic, keywords }),
      // });
      // const data: ContextRetrievalResponse = await response.json();
      // setContexts(data.contexts);

      // モックレスポンス
      const mockResponse: ContextRetrievalResponse = {
        topic,
        keywords: keywords || [],
        count: MOCK_CONTEXTS.length,
        contexts: MOCK_CONTEXTS
      };

      setContexts(mockResponse.contexts);
    } catch (err) {
      setError('背景知識の取得に失敗しました。ネットワーク接続を確認してください。');
      console.error('Context retrieval error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearContexts = () => {
    setContexts([]);
    setError(null);
  };

  return { contexts, loading, error, retrieveContext, clearContexts };
}
