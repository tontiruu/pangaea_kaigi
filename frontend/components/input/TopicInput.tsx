/**
 * Topic Input Component
 */
'use client';

import { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faComments, faRocket, faCircleNotch, faCheckCircle } from '@fortawesome/free-solid-svg-icons';
import { useContextRetrieval } from '@/hooks/useContextRetrieval';
import { ContextPanel } from '@/components/context/ContextPanel';
import { MCPConfigModal } from '@/components/context/MCPConfigModal';
import { SourceInfo } from '@/types/context';

interface TopicInputProps {
  onSubmit: (topic: string) => void;
  disabled?: boolean;
}

// Mock data
const MOCK_SOURCES: SourceInfo[] = [
  { name: 'Notion', enabled: true, description: 'Retrieve information from documents and knowledge base' },
  { name: 'Slack', enabled: false, description: 'Retrieve information from channel conversation history' },
  { name: 'Atlassian', enabled: true, description: 'Retrieve information from Jira/Confluence' }
];

export function TopicInput({ onSubmit, disabled }: TopicInputProps) {
  const [topic, setTopic] = useState('');
  const [hasRetrieved, setHasRetrieved] = useState(false);
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [sources, setSources] = useState<SourceInfo[]>(MOCK_SOURCES);
  const { contexts, loading, error, retrieveContext } = useContextRetrieval();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim()) {
      onSubmit(topic.trim());
    }
  };

  const handleRetrieveContext = async () => {
    if (topic.trim()) {
      // First show config modal
      setShowConfigModal(true);
    }
  };

  const handleConfigComplete = async () => {
    // Retrieve background knowledge after modal completion
    if (topic.trim()) {
      await retrieveContext(topic.trim());
      setHasRetrieved(true);
    }
  };

  const handleStartDiscussion = () => {
    if (topic.trim()) {
      onSubmit(topic.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="glass rounded-3xl shadow-2xl p-8 border border-white/30 transition-all duration-500 hover:shadow-[0_25px_50px_-12px_rgba(0,212,168,0.25)]">
        <div className="text-center mb-8">
          <div
            className="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4 shadow-xl transition-all duration-500 hover:scale-110 hover:rotate-12 animate-float-up"
            style={{ background: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))' }}
          >
            <FontAwesomeIcon icon={faComments} className="text-white text-3xl" />
          </div>
          <h2
            className="text-3xl font-bold mb-2 bg-clip-text text-transparent animate-fade-in"
            style={{ backgroundImage: 'linear-gradient(to right, var(--primary-dark), var(--primary), var(--primary-light))', animationDelay: '0.1s' }}
          >
            Enter the topic you want to discuss
          </h2>
          <p className="text-sm text-gray-600 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            AI agents will develop the discussion from multiple perspectives
          </p>
        </div>

        <div className="relative mb-6 animate-scale-in" style={{ animationDelay: '0.3s' }}>
          <textarea
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            disabled={disabled}
            placeholder="Example: About the direction of new business"
            className="w-full h-40 px-5 py-4 bg-white/60 backdrop-blur-sm border-2 border-white/50 rounded-2xl focus:ring-4 transition-all duration-500 resize-none disabled:bg-gray-100/50 disabled:cursor-not-allowed text-gray-800 placeholder:text-gray-400 shadow-inner hover:shadow-lg focus:shadow-xl"
            style={{
              '--tw-ring-color': 'rgba(0, 212, 168, 0.2)'
            } as React.CSSProperties}
            onFocus={(e) => {
              e.target.style.borderColor = 'var(--primary)';
              e.target.style.transform = 'scale(1.01)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'rgba(255, 255, 255, 0.5)';
              e.target.style.transform = 'scale(1)';
            }}
          />
          <div className="absolute bottom-3 right-3 text-xs font-medium transition-colors duration-300" style={{ color: topic.length > 0 ? 'var(--primary)' : 'var(--neutral-400)' }}>
            {topic.length} characters
          </div>
        </div>

        {/* Context panel or button */}
        <div className="animate-scale-in" style={{ animationDelay: '0.4s' }}>
          <ContextPanel
            contexts={contexts}
            loading={loading}
            error={error}
            onRetrieve={handleRetrieveContext}
            onStartDiscussion={handleStartDiscussion}
            hasRetrieved={hasRetrieved}
          />
        </div>

        <div className="mt-6 flex items-center justify-center gap-2 text-xs text-gray-500 animate-fade-in" style={{ animationDelay: '0.6s' }}>
          <FontAwesomeIcon icon={faCheckCircle} className="animate-pulse" style={{ color: 'var(--primary)' }} />
          <span>Ready - can start anytime</span>
        </div>
      </div>

      {/* MCP config modal */}
      <MCPConfigModal
        isOpen={showConfigModal}
        onClose={() => setShowConfigModal(false)}
        onComplete={handleConfigComplete}
        sources={sources}
      />
    </form>
  );
}
