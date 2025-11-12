/**
 * Chat Container Component
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
    <div className="flex-1 overflow-y-auto p-8">
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-gray-400">
          <div className="w-20 h-20 rounded-2xl flex items-center justify-center mb-6 shadow-lg animate-float-up" style={{ background: 'linear-gradient(to bottom right, rgba(0, 212, 168, 0.2), rgba(51, 224, 186, 0.2))' }}>
            <div className="w-4 h-4 rounded-full animate-pulse" style={{ background: 'linear-gradient(to right, var(--primary), var(--primary-light))' }}></div>
          </div>
          <p className="text-lg font-medium text-gray-500 mb-2 animate-fade-in" style={{ animationDelay: '0.2s' }}>Preparing for discussion</p>
          <p className="text-sm text-gray-400 animate-fade-in" style={{ animationDelay: '0.4s' }}>Starting soon...</p>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto">
          {messages.map((message, index) => (
            <div
              key={message.id}
              style={{
                animationDelay: `${Math.min(index * 50, 1000)}ms`
              }}
            >
              <MessageBubble message={message} />
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}
