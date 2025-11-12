/**
 * チャットコンテナコンポーネント
 */
'use client';

import { useEffect, useRef } from 'react';
import { Message } from '@/types/message';
import { MessageBubble } from './MessageBubble';

interface ChatContainerProps {
  messages: Message[];
}

export function ChatContainer({ messages }: ChatContainerProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-400">
          <p>議論が始まるまでお待ちください...</p>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}
