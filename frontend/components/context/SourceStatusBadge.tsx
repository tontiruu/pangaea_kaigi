/**
 * ソース状態表示バッジコンポーネント
 */
'use client';

import { useEffect, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCheckCircle,
  faTimesCircle,
  faFileAlt,
  faComments,
  faTasks,
  faChevronDown,
  faChevronUp,
  faCog,
} from '@fortawesome/free-solid-svg-icons';
import { SourceInfo } from '@/types/context';
import { MCPConfigModal } from './MCPConfigModal';

// モックデータ
const MOCK_SOURCES: SourceInfo[] = [
  {
    name: 'Notion',
    enabled: true,
    description: 'ドキュメントとナレッジベースから情報を取得'
  },
  {
    name: 'Slack',
    enabled: false,
    description: 'チャンネルの会話履歴から情報を取得'
  },
  {
    name: 'Atlassian',
    enabled: true,
    description: 'Jira/Confluenceから情報を取得'
  }
];

const SOURCE_ICONS = {
  'Notion': faFileAlt,
  'Slack': faComments,
  'Atlassian': faTasks
} as const;

export function SourceStatusBadge() {
  const [sources, setSources] = useState<SourceInfo[]>([]);
  const [expanded, setExpanded] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showConfigModal, setShowConfigModal] = useState(false);

  useEffect(() => {
    // モック: APIコールのシミュレーション
    const fetchSources = async () => {
      setLoading(true);
      await new Promise((resolve) => setTimeout(resolve, 500));

      // 実際のAPIコール（将来の実装用）
      // const response = await fetch('/api/context/sources');
      // const data = await response.json();
      // setSources(data.sources);

      setSources(MOCK_SOURCES);
      setLoading(false);
    };

    fetchSources();
  }, []);

  const enabledCount = sources.filter(s => s.enabled).length;

  const handleSourceClick = (source: SourceInfo) => {
    if (!source.enabled) {
      setExpanded(false);
      setShowConfigModal(true);
    }
  };

  const handleConfigComplete = () => {
    // モック: 実際はAPIから最新の状態を取得
    setSources(MOCK_SOURCES);
  };

  if (loading) {
    return (
      <div className="glass rounded-xl px-4 py-2 border border-white/30 animate-pulse">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-gray-300"></div>
          <div className="w-24 h-4 bg-gray-300 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* バッジボタン */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="bg-white rounded-xl px-4 py-2 border border-gray-200 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105 flex items-center gap-2 group"
      >
        <div className="flex items-center gap-2">
          <FontAwesomeIcon
            icon={enabledCount > 0 ? faCheckCircle : faTimesCircle}
            className="text-sm"
            style={{ color: enabledCount > 0 ? 'var(--primary)' : 'var(--neutral-400)' }}
          />
          <span className="text-xs font-semibold text-gray-700">
            MCP連携: {enabledCount}/{sources.length}
          </span>
        </div>
        <FontAwesomeIcon
          icon={expanded ? faChevronUp : faChevronDown}
          className="text-xs text-gray-500 transition-transform duration-300 group-hover:scale-110"
        />
      </button>

      {/* 展開パネル */}
      {expanded && (
        <div className="absolute top-full right-0 mt-2 w-80 bg-white rounded-2xl border border-gray-200 shadow-2xl p-4 z-50 animate-card-pop">
          <h3 className="font-bold text-sm text-gray-800 mb-3 flex items-center gap-2">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center shadow-md"
              style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}
            >
              <FontAwesomeIcon icon={faCheckCircle} className="text-white text-sm" />
            </div>
            背景知識連携設定
          </h3>

          <div className="space-y-2">
            {sources.map((source, index) => (
              <div
                key={source.name}
                className={`p-3 bg-gray-50 rounded-xl border border-gray-200 transition-all duration-300 hover:bg-gray-100 hover:shadow-md animate-slide-in ${
                  !source.enabled ? 'cursor-pointer' : ''
                }`}
                style={{ animationDelay: `${index * 50}ms` }}
                onClick={() => handleSourceClick(source)}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-9 h-9 rounded-lg flex items-center justify-center shadow-md transition-all duration-300 ${
                      source.enabled ? 'hover:scale-110' : 'opacity-50'
                    }`}
                    style={{
                      background: source.enabled
                        ? 'linear-gradient(to bottom right, var(--primary-light), var(--primary-dark))'
                        : 'linear-gradient(to bottom right, var(--neutral-300), var(--neutral-400))'
                    }}
                  >
                    <FontAwesomeIcon
                      icon={SOURCE_ICONS[source.name as keyof typeof SOURCE_ICONS]}
                      className="text-white text-sm"
                    />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-semibold text-sm text-gray-800">
                        {source.name}
                      </span>
                      <span
                        className={`px-2 py-0.5 text-xs font-bold rounded-full ${
                          source.enabled
                            ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white'
                            : 'bg-gray-300 text-gray-600'
                        }`}
                      >
                        {source.enabled ? '設定済み' : '未設定'}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 leading-relaxed">
                      {source.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 pt-3 border-t border-gray-200 flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-gray-600">
              <FontAwesomeIcon icon={faCheckCircle} style={{ color: 'var(--primary)' }} />
              <span>
                Dedalus Labs API: <span className="font-semibold">設定済み</span>
              </span>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setExpanded(false);
                setShowConfigModal(true);
              }}
              className="px-3 py-1.5 rounded-lg bg-white border border-gray-200 hover:bg-gray-50 transition-all duration-300 flex items-center gap-2 text-xs font-semibold text-gray-700 hover:scale-105"
            >
              <FontAwesomeIcon icon={faCog} />
              設定
            </button>
          </div>
        </div>
      )}

      {/* 設定モーダル */}
      <MCPConfigModal
        isOpen={showConfigModal}
        onClose={() => setShowConfigModal(false)}
        onComplete={handleConfigComplete}
        sources={sources}
      />
    </div>
  );
}
