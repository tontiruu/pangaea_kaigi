/**
 * コンテキストカードコンポーネント
 */
'use client';

import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faFileAlt,
  faComments as faSlack,
  faTasks,
  faChevronDown,
  faChevronUp,
  faExternalLinkAlt,
} from '@fortawesome/free-solid-svg-icons';
import { ContextItem, SourceType } from '@/types/context';

interface ContextCardProps {
  context: ContextItem;
  index: number;
}

const SOURCE_CONFIG = {
  notion: {
    icon: faFileAlt,
    label: 'Notion',
    gradient: 'linear-gradient(to bottom right, #1F1F1F, #000000)',
    bgColor: 'from-neutral-50 to-neutral-100',
    borderColor: 'var(--neutral-400)'
  },
  slack: {
    icon: faSlack,
    label: 'Slack',
    gradient: 'linear-gradient(to bottom right, #611f69, #4A154B)',
    bgColor: 'from-purple-50 to-fuchsia-100',
    borderColor: '#611f69'
  },
  atlassian: {
    icon: faTasks,
    label: 'Atlassian',
    gradient: 'linear-gradient(to bottom right, #0052CC, #0747A6)',
    bgColor: 'from-blue-50 to-indigo-100',
    borderColor: '#0052CC'
  }
} as const;

export function ContextCard({ context, index }: ContextCardProps) {
  const [expanded, setExpanded] = useState(false);
  const config = SOURCE_CONFIG[context.source];

  const truncateContent = (text: string, maxLength: number) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div
      className={`bg-gradient-to-br ${config.bgColor} rounded-2xl p-5 border border-gray-200 shadow-md hover:shadow-xl hover:-translate-y-1 hover:scale-[1.01] transition-all duration-500 animate-card-lift cursor-pointer`}
      style={{
        borderLeft: `4px solid ${config.borderColor}`,
        animationDelay: `${index * 100}ms`
      }}
      onClick={() => setExpanded(!expanded)}
    >
      <div className="flex items-start gap-4">
        {/* ソースアイコン */}
        <div
          className="flex-shrink-0 w-11 h-11 rounded-xl flex items-center justify-center shadow-lg ring-2 ring-white/50 transition-all duration-300 hover:scale-110 hover:rotate-6"
          style={{ background: config.gradient }}
        >
          <FontAwesomeIcon icon={config.icon} className="text-white text-lg" />
        </div>

        {/* コンテンツ */}
        <div className="flex-1 min-w-0">
          {/* ヘッダー */}
          <div className="flex items-start justify-between gap-3 mb-2">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span
                  className="px-2 py-0.5 text-xs font-bold text-white rounded-full shadow-sm"
                  style={{ background: config.gradient }}
                >
                  {config.label}
                </span>
                {context.metadata?.section && (
                  <span className="text-xs text-gray-500">
                    {context.metadata.section}
                  </span>
                )}
              </div>
              <h3 className="font-bold text-sm text-gray-800 leading-snug">
                {context.title}
              </h3>
            </div>

            {/* 展開ボタン */}
            <button
              className="flex-shrink-0 w-8 h-8 rounded-lg bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-all duration-300 hover:scale-110 shadow-sm"
              onClick={(e) => {
                e.stopPropagation();
                setExpanded(!expanded);
              }}
            >
              <FontAwesomeIcon
                icon={expanded ? faChevronUp : faChevronDown}
                className="text-gray-600 text-sm"
              />
            </button>
          </div>

          {/* コンテンツ */}
          <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
            {expanded ? context.content : truncateContent(context.content, 150)}
          </p>

          {/* URL */}
          {context.url && (
            <a
              href={context.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 mt-3 text-xs font-medium hover:underline transition-colors duration-300"
              style={{ color: config.borderColor }}
              onClick={(e) => e.stopPropagation()}
            >
              <FontAwesomeIcon icon={faExternalLinkAlt} className="text-xs" />
              リンクを開く
            </a>
          )}

          {/* メタデータ */}
          {expanded && context.metadata && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              <div className="flex flex-wrap gap-2">
                {Object.entries(context.metadata)
                  .filter(([key]) => key !== 'section')
                  .map(([key, value]) => (
                    <div
                      key={key}
                      className="px-2 py-1 bg-white border border-gray-200 rounded-lg text-xs text-gray-600 shadow-sm"
                    >
                      <span className="font-semibold">{key}:</span> {String(value)}
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
