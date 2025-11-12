/**
 * メッセージ吹き出しコンポーネント
 */
import { Message, MessageType } from '@/types/message';

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const getMessageStyle = () => {
    switch (message.message_type) {
      case MessageType.SYSTEM:
        return 'bg-gray-100 text-gray-800 border-l-4 border-gray-400';
      case MessageType.OPINION:
        return 'bg-blue-50 text-blue-900 border-l-4 border-blue-500';
      case MessageType.PERSUASION:
        return 'bg-green-50 text-green-900 border-l-4 border-green-500';
      case MessageType.RESPONSE:
        return 'bg-purple-50 text-purple-900 border-l-4 border-purple-500';
      case MessageType.CONCLUSION:
        return 'bg-yellow-50 text-yellow-900 border-l-4 border-yellow-500';
      default:
        return 'bg-white text-gray-800 border-l-4 border-gray-300';
    }
  };

  const getMessageTypeLabel = () => {
    switch (message.message_type) {
      case MessageType.SYSTEM:
        return 'システム';
      case MessageType.OPINION:
        return '意見';
      case MessageType.PERSUASION:
        return '説得';
      case MessageType.RESPONSE:
        return '応答';
      case MessageType.CONCLUSION:
        return '結論';
      default:
        return '';
    }
  };

  return (
    <div className={`p-4 rounded-lg mb-3 ${getMessageStyle()} shadow-sm`}>
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-bold">
            {message.agent_name.charAt(0)}
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-semibold text-sm">{message.agent_name}</span>
            {message.message_type !== MessageType.SYSTEM && (
              <span className="text-xs px-2 py-0.5 bg-white bg-opacity-50 rounded">
                {getMessageTypeLabel()}
              </span>
            )}
            <span className="text-xs text-gray-500 ml-auto">
              {new Date(message.timestamp).toLocaleTimeString('ja-JP')}
            </span>
          </div>
          <div className="text-sm whitespace-pre-wrap break-words">
            {message.content}
          </div>
        </div>
      </div>
    </div>
  );
}
