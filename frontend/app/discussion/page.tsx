/**
 * 議論ページ
 */
'use client';

import { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { TopicInput } from '@/components/input/TopicInput';
import { ChatContainer } from '@/components/chat/ChatContainer';

export default function DiscussionPage() {
  const [started, setStarted] = useState(false);
  const wsUrl = 'ws://localhost:8000/ws/discussion';

  const {
    connected,
    topic,
    agenda,
    agents,
    messages,
    currentPhase,
    currentAgendaIndex,
    finalConclusion,
    error,
    connect,
    startDiscussion,
  } = useWebSocket(wsUrl);

  useEffect(() => {
    connect();
  }, [connect]);

  const handleStartDiscussion = (newTopic: string) => {
    setStarted(true);
    startDiscussion(newTopic);
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* ヘッダー */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              Pangaea Kaigi - AI会議システム
            </h1>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div
                  className={`w-2 h-2 rounded-full ${
                    connected ? 'bg-green-500' : 'bg-red-500'
                  }`}
                />
                <span className="text-sm text-gray-600">
                  {connected ? '接続中' : '切断'}
                </span>
              </div>
            </div>
          </div>
          {topic && (
            <div className="mt-2 text-sm text-gray-600">
              議題: <span className="font-semibold">{topic}</span>
            </div>
          )}
        </div>
      </header>

      {/* サイドバー: アジェンダと参加者 */}
      {started && (
        <div className="flex flex-1 overflow-hidden">
          <aside className="w-80 bg-white border-r overflow-y-auto">
            {/* アジェンダ */}
            {agenda.length > 0 && (
              <div className="p-4 border-b">
                <h3 className="font-semibold text-gray-700 mb-3">アジェンダ</h3>
                <div className="space-y-2">
                  {agenda.map((item, index) => (
                    <div
                      key={item.id}
                      className={`p-3 rounded-lg text-sm ${
                        index === currentAgendaIndex
                          ? 'bg-blue-50 border-2 border-blue-500'
                          : 'bg-gray-50'
                      }`}
                    >
                      <div className="font-medium">
                        {item.order}. {item.title}
                      </div>
                      <div className="text-xs text-gray-600 mt-1">
                        {item.description}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 参加者 */}
            {agents.length > 0 && (
              <div className="p-4">
                <h3 className="font-semibold text-gray-700 mb-3">
                  参加者 ({agents.length}名)
                </h3>
                <div className="space-y-2">
                  {agents.map((agent) => (
                    <div
                      key={agent.id}
                      className="p-3 bg-gray-50 rounded-lg text-sm"
                    >
                      <div className="font-medium">{agent.name}</div>
                      <div className="text-xs text-gray-600 mt-1">
                        {agent.perspective}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </aside>

          {/* メインチャットエリア */}
          <main className="flex-1 flex flex-col">
            {/* フェーズ表示 */}
            {currentPhase && (
              <div className="bg-blue-50 px-6 py-3 border-b">
                <div className="text-sm text-blue-800">
                  現在のフェーズ:{' '}
                  <span className="font-semibold">
                    {currentPhase === 'independent_opinions' && '独立意見出し'}
                    {currentPhase === 'voting' && '投票'}
                    {currentPhase === 'persuasion' && '説得プロセス'}
                    {currentPhase === 'agenda_creation' && 'アジェンダ作成'}
                    {currentPhase === 'agent_generation' && '参加者選定'}
                  </span>
                </div>
              </div>
            )}

            <ChatContainer messages={messages} />

            {/* 最終結論 */}
            {finalConclusion && (
              <div className="bg-green-50 p-6 border-t">
                <h3 className="font-semibold text-green-800 mb-2">
                  最終結論
                </h3>
                <div className="text-sm text-green-900 whitespace-pre-wrap">
                  {finalConclusion}
                </div>
              </div>
            )}
          </main>
        </div>
      )}

      {/* 初期画面: 議題入力 */}
      {!started && (
        <div className="flex-1 flex items-center justify-center p-6">
          <TopicInput
            onSubmit={handleStartDiscussion}
            disabled={!connected || started}
          />
        </div>
      )}

      {/* エラー表示 */}
      {error && (
        <div className="fixed bottom-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg">
          {error}
        </div>
      )}
    </div>
  );
}
