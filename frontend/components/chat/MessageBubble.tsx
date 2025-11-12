/**
 * メッセージ吹き出しコンポーネント
 */
import { Message, MessageType } from '@/types/message';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCog,
  faLightbulb,
  faComments,
  faComment,
  faStar,
  faFileAlt,
} from '@fortawesome/free-solid-svg-icons';

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const getMessageStyle = () => {
    switch (message.message_type) {
      case MessageType.SYSTEM:
        return {
          container: 'bg-gradient-to-br from-neutral-50 to-neutral-100 shadow-md',
          borderColor: 'var(--neutral-400)',
          badge: 'bg-neutral-500',
          avatarGradient: 'linear-gradient(to bottom right, var(--neutral-400), var(--neutral-500))',
          icon: faCog
        };
      case MessageType.OPINION:
        return {
          container: 'bg-gradient-to-br from-teal-50 to-emerald-100 shadow-md',
          borderColor: 'var(--primary)',
          badge: 'bg-gradient-to-r from-teal-500 to-emerald-500',
          avatarGradient: 'linear-gradient(to bottom right, var(--primary-light), var(--primary))',
          icon: faLightbulb
        };
      case MessageType.PERSUASION:
        return {
          container: 'bg-gradient-to-br from-emerald-50 to-teal-100 shadow-md',
          borderColor: 'var(--primary-dark)',
          badge: 'bg-gradient-to-r from-emerald-500 to-teal-600',
          avatarGradient: 'linear-gradient(to bottom right, var(--primary), var(--primary-dark))',
          icon: faComments
        };
      case MessageType.RESPONSE:
        return {
          container: 'bg-gradient-to-br from-cyan-50 to-teal-100 shadow-md',
          borderColor: 'var(--primary-light)',
          badge: 'bg-gradient-to-r from-cyan-500 to-teal-500',
          avatarGradient: 'linear-gradient(to bottom right, var(--primary-lighter), var(--primary-light))',
          icon: faComment
        };
      case MessageType.CONCLUSION:
        return {
          container: 'bg-gradient-to-br from-emerald-50 to-green-100 shadow-md',
          borderColor: 'var(--primary)',
          badge: 'bg-gradient-to-r from-emerald-500 to-green-600',
          avatarGradient: 'linear-gradient(to bottom right, var(--primary), var(--primary-darker))',
          icon: faStar
        };
      default:
        return {
          container: 'bg-white/70 backdrop-blur-sm shadow-md',
          borderColor: 'var(--neutral-300)',
          badge: 'bg-neutral-400',
          avatarGradient: 'linear-gradient(to bottom right, var(--neutral-400), var(--neutral-500))',
          icon: faFileAlt
        };
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

  const style = getMessageStyle();

  return (
    <div
      className={`p-5 rounded-2xl mb-4 ${style.container} backdrop-blur-sm border border-white/30 transition-all duration-500 hover:shadow-2xl hover:scale-[1.02] hover:-translate-y-1 animate-card-lift`}
      style={{
        borderLeft: `4px solid ${style.borderColor}`
      }}
    >
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          <div
            className="w-11 h-11 rounded-xl flex items-center justify-center text-white font-bold shadow-lg ring-2 ring-white/50 transition-all duration-300 hover:scale-110 hover:rotate-6"
            style={{
              background: style.avatarGradient
            }}
          >
            <FontAwesomeIcon icon={style.icon} className="text-lg" />
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span className="font-bold text-sm text-gray-800">{message.agent_name}</span>
            {message.message_type !== MessageType.SYSTEM && (
              <span className={`text-xs px-2.5 py-1 text-white rounded-full font-medium shadow-sm ${style.badge}`}>
                {getMessageTypeLabel()}
              </span>
            )}
            <span className="text-xs text-gray-500 ml-auto font-medium">
              {new Date(message.timestamp).toLocaleTimeString('ja-JP')}
            </span>
          </div>
          <div className="text-sm text-gray-800 whitespace-pre-wrap break-words leading-relaxed">
            {message.content}
          </div>
        </div>
      </div>
    </div>
  );
}
