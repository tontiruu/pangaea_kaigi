/**
 * メッセージ型定義
 */

export enum MessageType {
  SYSTEM = "system",
  OPINION = "opinion",
  VOTE = "vote",
  PERSUASION = "persuasion",
  RESPONSE = "response",
  CONCLUSION = "conclusion",
}

export interface Message {
  id: string;
  agent_id: string;
  agent_name: string;
  content: string;
  message_type: MessageType;
  timestamp: string;
}

export interface Opinion {
  id: string;
  agent_id: string;
  agent_name: string;
  content: string;
  votes: number;
}
