/**
 * 背景知識パネルコンポーネント
 */
'use client';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faLightbulb,
  faCircleNotch,
  faExclamationTriangle,
  faCheckCircle,
} from '@fortawesome/free-solid-svg-icons';
import { ContextItem } from '@/types/context';
import { ContextCard } from './ContextCard';

interface ContextPanelProps {
  contexts: ContextItem[];
  loading: boolean;
  error: string | null;
  onRetrieve: () => void;
  onStartDiscussion: () => void;
  hasRetrieved: boolean;
}

export function ContextPanel({
  contexts,
  loading,
  error,
  onRetrieve,
  onStartDiscussion,
  hasRetrieved
}: ContextPanelProps) {
  return (
    <div className="w-full">
      {/* 取得前: ボタン表示 */}
      {!hasRetrieved && !loading && (
        <div className="flex gap-3 animate-scale-in" style={{ animationDelay: '0.5s' }}>
          {/* <button
            onClick={onRetrieve}
            className="flex-1 px-6 py-3 rounded-2xl font-bold text-gray-800 bg-white border-2 border-gray-200 shadow-md hover:shadow-xl hover:scale-[1.02] hover:-translate-y-0.5 transition-all duration-500 flex items-center justify-center gap-2 group"
          >
            <FontAwesomeIcon
              icon={faLightbulb}
              className="text-lg transition-transform duration-300 group-hover:rotate-12"
              style={{ color: 'var(--accent-warning)' }}
            />
            背景知識を取得
          </button> */}
          <button
            onClick={onStartDiscussion}
            className="flex-1 px-6 py-3 rounded-2xl font-bold text-white hover:shadow-2xl hover:scale-[1.02] hover:-translate-y-0.5 transition-all duration-500 flex items-center justify-center gap-2"
            style={{
              background: 'linear-gradient(to right, var(--primary-dark), var(--primary), var(--primary-light))'
            }}
          >
            <span className="text-lg">▶</span>
            議論を開始
          </button>
        </div>
      )}

      {/* 取得中: ローディング */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-12 animate-float-up">
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4 shadow-xl"
            style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}
          >
            <FontAwesomeIcon icon={faCircleNotch} className="text-white text-2xl animate-spin" />
          </div>
          <p className="text-lg font-semibold text-gray-700 mb-2">背景知識を取得中...</p>
          <p className="text-sm text-gray-500">関連情報を検索しています</p>
        </div>
      )}

      {/* エラー表示 */}
      {error && !loading && (
        <div className="p-6 rounded-2xl bg-gradient-to-br from-red-50 to-pink-50 border-2 border-red-200 animate-card-pop">
          <div className="flex items-start gap-3">
            <FontAwesomeIcon icon={faExclamationTriangle} className="text-red-500 text-xl mt-1" />
            <div>
              <h3 className="font-bold text-red-800 mb-1">エラーが発生しました</h3>
              <p className="text-sm text-red-700">{error}</p>
              <button
                onClick={onRetrieve}
                className="mt-3 px-4 py-2 rounded-xl bg-red-500 text-white text-sm font-semibold hover:bg-red-600 transition-colors duration-300"
              >
                再試行
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 取得後: コンテキスト表示 */}
      {hasRetrieved && !loading && !error && contexts.length > 0 && (
        <div className="space-y-4">
          {/* ヘッダー */}
          <div className="flex items-center justify-between animate-fade-in">
            <div className="flex items-center gap-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center shadow-lg"
                style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}
              >
                <FontAwesomeIcon icon={faCheckCircle} className="text-white text-lg" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-gray-800">
                  背景知識（{contexts.length}件）
                </h3>
                <p className="text-xs text-gray-500">
                  議論に関連する情報を取得しました
                </p>
              </div>
            </div>
          </div>

          {/* コンテキストカード一覧 */}
          <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
            {contexts.map((context, index) => (
              <ContextCard key={index} context={context} index={index} />
            ))}
          </div>

          {/* アクションボタン */}
          <div className="flex gap-3 pt-4 border-t border-gray-200 animate-scale-in" style={{ animationDelay: `${contexts.length * 100 + 200}ms` }}>
            <button
              onClick={onRetrieve}
              className="px-6 py-3 rounded-2xl font-semibold text-gray-700 bg-white border border-gray-200 shadow-md hover:shadow-lg transition-all duration-300"
            >
              再取得
            </button>
            <button
              onClick={onStartDiscussion}
              className="flex-1 px-6 py-3 rounded-2xl font-bold text-white hover:shadow-2xl hover:scale-[1.02] hover:-translate-y-0.5 transition-all duration-500 flex items-center justify-center gap-2 group"
              style={{
                background: 'linear-gradient(to right, var(--primary-dark), var(--primary), var(--primary-light))'
              }}
            >
              <span className="text-lg group-hover:scale-110 transition-transform duration-300">▶</span>
              この背景知識を使って議論を開始
            </button>
          </div>
        </div>
      )}

      {/* 結果なし */}
      {hasRetrieved && !loading && !error && contexts.length === 0 && (
        <div className="p-8 rounded-2xl bg-gradient-to-br from-gray-50 to-neutral-100 border border-white/30 text-center animate-scale-in">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
            <FontAwesomeIcon icon={faLightbulb} className="text-gray-500 text-2xl" />
          </div>
          <h3 className="font-bold text-gray-700 mb-2">背景知識が見つかりませんでした</h3>
          <p className="text-sm text-gray-600 mb-4">
            このトピックに関連する情報が取得できませんでした
          </p>
          <button
            onClick={onStartDiscussion}
            className="px-6 py-3 rounded-2xl font-bold text-white hover:shadow-xl transition-all duration-300"
            style={{
              background: 'linear-gradient(to right, var(--primary-dark), var(--primary))'
            }}
          >
            背景知識なしで議論を開始
          </button>
        </div>
      )}
    </div>
  );
}
