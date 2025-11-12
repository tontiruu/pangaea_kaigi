/**
 * WebSocket接続を管理するカスタムフック
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { Message } from '@/types/message';
import { Agent } from '@/types/agent';
import { AgendaItem } from '@/types/discussion';

interface WebSocketMessage {
  type: string;
  data: any;
}

interface VoteDetail {
  voter_id: string;
  voter_name: string;
  opinion_id: string;
}

interface OpinionDetail {
  id: string;
  agent_id: string;
  agent_name: string;
  content: string;
  votes: number;
}

interface VotingResult {
  votes: Record<string, number>;
  vote_details: VoteDetail[];
  opinions: OpinionDetail[];
  remaining_opinions: number;
}

export interface DiscussionState {
  connected: boolean;
  discussionId: string | null;
  topic: string | null;
  agenda: AgendaItem[];
  agents: Agent[];
  messages: Message[];
  currentPhase: string | null;
  currentAgendaIndex: number;
  votingResult: VotingResult | null;
  finalConclusion: string | null;
  agendaStreaming: string | null;
  error: string | null;
}

export function useWebSocket(url: string) {
  const [state, setState] = useState<DiscussionState>({
    connected: false,
    discussionId: null,
    topic: null,
    agenda: [],
    agents: [],
    messages: [],
    currentPhase: null,
    currentAgendaIndex: 0,
    votingResult: null,
    finalConclusion: null,
    agendaStreaming: null,
    error: null,
  });

  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const ws = new WebSocket(url);

    ws.onopen = () => {
      console.log('WebSocket接続成功');
      setState(prev => ({ ...prev, connected: true, error: null }));
    };

    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        handleMessage(message);
      } catch (error) {
        console.error('メッセージ解析エラー:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocketエラー:', error);
      setState(prev => ({ ...prev, error: 'WebSocket接続エラー' }));
    };

    ws.onclose = () => {
      console.log('WebSocket切断');
      setState(prev => ({ ...prev, connected: false }));
    };

    wsRef.current = ws;
  }, [url]);

  const handleMessage = useCallback((message: WebSocketMessage) => {
    console.log('受信:', message.type, message.data);

    switch (message.type) {
      case 'discussion_started':
        setState(prev => ({
          ...prev,
          discussionId: message.data.discussion_id,
          topic: message.data.topic,
        }));
        break;

      case 'agenda_streaming':
        setState(prev => ({
          ...prev,
          agendaStreaming: message.data.content,
        }));
        break;

      case 'agenda_created':
        setState(prev => ({
          ...prev,
          agenda: message.data.agenda,
          agendaStreaming: null, // ストリーミング完了
        }));
        break;

      case 'agents_created':
        setState(prev => ({
          ...prev,
          agents: message.data.agents,
        }));
        break;

      case 'phase_changed':
        setState(prev => ({
          ...prev,
          currentPhase: message.data.phase,
          currentAgendaIndex: message.data.agenda_index || prev.currentAgendaIndex,
        }));
        break;

      case 'message':
        setState(prev => {
          // Check if message with same ID already exists
          const existingIndex = prev.messages.findIndex(m => m.id === message.data.id);
          if (existingIndex !== -1) {
            // Update existing message
            const updatedMessages = [...prev.messages];
            updatedMessages[existingIndex] = message.data;
            return {
              ...prev,
              messages: updatedMessages,
            };
          }
          // Add new message
          return {
            ...prev,
            messages: [...prev.messages, message.data],
          };
        });
        break;

      case 'voting_result':
        setState(prev => ({
          ...prev,
          votingResult: message.data,
        }));
        break;

      case 'agenda_completed':
        // アジェンダ完了の処理
        break;

      case 'discussion_completed':
        setState(prev => ({
          ...prev,
          finalConclusion: message.data.final_conclusion,
        }));
        break;

      case 'error':
        setState(prev => ({
          ...prev,
          error: message.data.message,
        }));
        break;

      default:
        console.log('未知のメッセージタイプ:', message.type);
    }
  }, []);

  const startDiscussion = useCallback((topic: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.error('WebSocketが接続されていません');
      return;
    }

    wsRef.current.send(JSON.stringify({
      type: 'start_discussion',
      data: { topic },
    }));
  }, []);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    ...state,
    connect,
    disconnect,
    startDiscussion,
  };
}
