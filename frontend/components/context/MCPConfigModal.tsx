/**
 * MCP Configuration Modal Component
 */
'use client';

import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faTimes,
  faCheckCircle,
  faCircle,
  faPlus,
  faKey,
  faGlobe,
  faExternalLinkAlt,
} from '@fortawesome/free-solid-svg-icons';
import { SourceInfo } from '@/types/context';
import Image from 'next/image';

interface MCPConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: () => void;
  sources: SourceInfo[];
}

const SOURCE_CONFIG = {
  Notion: {
    iconPath: '/tool/notion.png',
    gradient: 'linear-gradient(to bottom right, #1F1F1F, #000000)',
    description: 'ドキュメントとナレッジベースから情報を取得',
    setupFields: [
      { name: 'api_key', label: 'API Key', type: 'password', placeholder: 'secret_xxxxxxxxxxxxxxxx' },
      { name: 'database_id', label: 'Database ID', type: 'text', placeholder: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' }
    ],
    docUrl: 'https://developers.notion.com/'
  },
  Slack: {
    iconPath: '/tool/slack.png',
    gradient: 'linear-gradient(to bottom right, #611f69, #4A154B)',
    description: 'チャンネルの会話履歴から情報を取得',
    setupFields: [
      { name: 'bot_token', label: 'Bot User OAuth Token', type: 'password', placeholder: 'xoxb-xxxxxxxxxxxxx' },
      { name: 'workspace', label: 'Workspace Name', type: 'text', placeholder: 'my-workspace' }
    ],
    docUrl: 'https://api.slack.com/apps'
  },
  Atlassian: {
    iconPath: '/tool/atlassian.png',
    gradient: 'linear-gradient(to bottom right, #0052CC, #0747A6)',
    description: 'Jira/Confluenceから情報を取得',
    setupFields: [
      { name: 'api_token', label: 'API Token', type: 'password', placeholder: 'ATATTxxxxxxxxxxxxxxxx' },
      { name: 'email', label: 'Email', type: 'email', placeholder: 'user@example.com' },
      { name: 'site_url', label: 'Site URL', type: 'url', placeholder: 'https://your-domain.atlassian.net' }
    ],
    docUrl: 'https://developer.atlassian.com/'
  }
} as const;

export function MCPConfigModal({ isOpen, onClose, onComplete, sources }: MCPConfigModalProps) {
  const [selectedSource, setSelectedSource] = useState<string | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});

  if (!isOpen) return null;

  const handleSourceClick = (sourceName: string) => {
    const source = sources.find(s => s.name === sourceName);
    if (!source?.enabled) {
      setSelectedSource(sourceName);
      setFormData({});
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSaveConnection = () => {
    // モック: 実際はAPIコールでデータを保存
    console.log('Saving connection for', selectedSource, formData);
    setSelectedSource(null);
    setFormData({});
    // TODO: 実際はAPI呼び出し後に onComplete() を実行
  };

  const handleComplete = () => {
    onComplete();
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in">
      {/* オーバーレイ */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* モーダル */}
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-white rounded-3xl shadow-2xl overflow-hidden animate-card-pop">
        {/* ヘッダー */}
        <div className="px-8 py-6 border-b border-gray-200" style={{ background: 'linear-gradient(to right, rgba(0, 212, 168, 0.05), rgba(51, 224, 186, 0.05))' }}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg"
                style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}
              >
                <FontAwesomeIcon icon={faKey} className="text-white text-xl" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">MCP連携設定</h2>
                <p className="text-sm text-gray-600">ナレッジソースとの連携を設定</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="w-10 h-10 rounded-xl bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-all duration-300 hover:scale-110"
            >
              <FontAwesomeIcon icon={faTimes} className="text-gray-600" />
            </button>
          </div>
        </div>

        {/* コンテンツ */}
        <div className="p-8 overflow-y-auto max-h-[calc(90vh-180px)]">
          {!selectedSource ? (
            // ソース一覧
            <div className="space-y-4">
              <div className="mb-6">
                <h3 className="text-lg font-bold text-gray-800 mb-2">連携可能なサービス</h3>
                <p className="text-sm text-gray-600">
                  背景知識を取得するためのサービスを設定してください
                </p>
              </div>

              {sources.map((source, index) => {
                const config = SOURCE_CONFIG[source.name as keyof typeof SOURCE_CONFIG];
                return (
                  <div
                    key={source.name}
                    className={`p-6 rounded-2xl border-2 transition-all duration-500 animate-card-lift ${
                      source.enabled
                        ? 'bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-200'
                        : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer'
                    }`}
                    style={{ animationDelay: `${index * 100}ms` }}
                    onClick={() => !source.enabled && handleSourceClick(source.name)}
                  >
                    <div className="flex items-start gap-4">
                      <div
                        className={`flex-shrink-0 w-14 h-14 rounded-xl flex items-center justify-center shadow-lg ring-2 ring-white transition-all duration-300 overflow-hidden bg-white ${
                          !source.enabled && 'hover:scale-110 hover:rotate-6'
                        }`}
                      >
                        <Image
                          src={config.iconPath}
                          alt={source.name}
                          width={56}
                          height={56}
                          className="object-contain p-1"
                        />
                      </div>

                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-bold text-gray-800">{source.name}</h3>
                          {source.enabled ? (
                            <div className="flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-xs font-bold rounded-full shadow-md">
                              <FontAwesomeIcon icon={faCheckCircle} />
                              設定済み
                            </div>
                          ) : (
                            <div className="flex items-center gap-1.5 px-3 py-1 bg-gray-200 text-gray-600 text-xs font-bold rounded-full">
                              <FontAwesomeIcon icon={faCircle} className="text-[8px]" />
                              未設定
                            </div>
                          )}
                        </div>
                        <p className="text-sm text-gray-600 mb-3">{config.description}</p>

                        {!source.enabled && (
                          <button
                            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl font-semibold text-sm text-white transition-all duration-300 hover:shadow-lg hover:scale-105"
                            style={{ background: config.gradient }}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleSourceClick(source.name);
                            }}
                          >
                            <FontAwesomeIcon icon={faPlus} />
                            連携を設定
                          </button>
                        )}

                        {source.enabled && (
                          <div className="flex items-center gap-2 text-xs text-gray-500">
                            <FontAwesomeIcon icon={faCheckCircle} style={{ color: 'var(--primary)' }} />
                            <span>このサービスは設定済みです</span>
                          </div>
                        )}
                      </div>

                      <a
                        href={config.docUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex-shrink-0 w-10 h-10 rounded-xl bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-all duration-300 hover:scale-110"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <FontAwesomeIcon icon={faExternalLinkAlt} className="text-gray-600 text-sm" />
                      </a>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            // 設定フォーム
            <div className="animate-scale-in">
              <button
                onClick={() => setSelectedSource(null)}
                className="mb-6 text-sm text-gray-600 hover:text-gray-800 font-medium transition-colors duration-300 flex items-center gap-2"
              >
                ← 戻る
              </button>

              {(() => {
                const config = SOURCE_CONFIG[selectedSource as keyof typeof SOURCE_CONFIG];
                return (
                  <div>
                    <div className="flex items-center gap-4 mb-6">
                      <div
                        className="w-16 h-16 rounded-xl flex items-center justify-center shadow-lg overflow-hidden bg-white"
                      >
                        <Image
                          src={config.iconPath}
                          alt={selectedSource}
                          width={64}
                          height={64}
                          className="object-contain p-1"
                        />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-gray-800">{selectedSource} 連携設定</h3>
                        <p className="text-sm text-gray-600">{config.description}</p>
                      </div>
                    </div>

                    <div className="space-y-4 mb-6">
                      {config.setupFields.map((field) => (
                        <div key={field.name}>
                          <label className="block text-sm font-semibold text-gray-700 mb-2">
                            {field.label}
                          </label>
                          <input
                            type={field.type}
                            placeholder={field.placeholder}
                            value={formData[field.name] || ''}
                            onChange={(e) => handleInputChange(field.name, e.target.value)}
                            className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-xl focus:border-primary focus:ring-4 transition-all duration-300 text-gray-800 placeholder:text-gray-400"
                            style={{
                              '--tw-ring-color': 'rgba(0, 212, 168, 0.2)'
                            } as React.CSSProperties}
                          />
                        </div>
                      ))}
                    </div>

                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-xl mb-6">
                      <div className="flex items-start gap-3">
                        <FontAwesomeIcon icon={faGlobe} className="text-blue-500 mt-1" />
                        <div className="flex-1">
                          <h4 className="text-sm font-semibold text-blue-800 mb-1">セットアップガイド</h4>
                          <p className="text-xs text-blue-700 mb-2">
                            {selectedSource}のAPI認証情報は、開発者ポータルから取得できます。
                          </p>
                          <a
                            href={config.docUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-700 transition-colors duration-300"
                          >
                            <FontAwesomeIcon icon={faExternalLinkAlt} />
                            ドキュメントを開く
                          </a>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-3">
                      <button
                        onClick={() => setSelectedSource(null)}
                        className="px-6 py-3 rounded-xl font-semibold text-gray-700 bg-gray-100 hover:bg-gray-200 transition-all duration-300"
                      >
                        キャンセル
                      </button>
                      <button
                        onClick={handleSaveConnection}
                        disabled={!Object.keys(formData).length}
                        className="flex-1 px-6 py-3 rounded-xl font-bold text-white transition-all duration-300 hover:shadow-xl hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                        style={{
                          background: 'linear-gradient(to right, var(--primary-dark), var(--primary), var(--primary-light))'
                        }}
                      >
                        保存して連携
                      </button>
                    </div>
                  </div>
                );
              })()}
            </div>
          )}
        </div>

        {/* フッター */}
        {!selectedSource && (
          <div className="px-8 py-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center justify-between">
              <div className="text-xs text-gray-600">
                <FontAwesomeIcon icon={faCheckCircle} style={{ color: 'var(--primary)' }} className="mr-2" />
                設定済み: {sources.filter(s => s.enabled).length}/{sources.length}
              </div>
              <button
                onClick={handleComplete}
                className="px-6 py-2 rounded-xl font-bold text-white transition-all duration-300 hover:shadow-lg hover:scale-105"
                style={{
                  background: 'linear-gradient(to right, var(--primary-dark), var(--primary))'
                }}
              >
                完了
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
