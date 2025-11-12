/**
 * 議題入力コンポーネント
 */
'use client';

import { useState } from 'react';

interface TopicInputProps {
  onSubmit: (topic: string) => void;
  disabled?: boolean;
}

export function TopicInput({ onSubmit, disabled }: TopicInputProps) {
  const [topic, setTopic] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim()) {
      onSubmit(topic.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">
          議論したい議題を入力してください
        </h2>
        <textarea
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          disabled={disabled}
          placeholder="例: 新規事業の方向性について"
          className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={disabled || !topic.trim()}
          className="mt-4 w-full bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {disabled ? '議論中...' : '議論を開始'}
        </button>
      </div>
    </form>
  );
}
