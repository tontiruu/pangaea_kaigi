/**
 * Agent型定義
 */

export enum AgentRole {
  FACILITATOR = "facilitator",
  PARTICIPANT = "participant",
}

export interface Agent {
  id: string;
  name: string;
  role: AgentRole;
  perspective: string;
  response_id?: string;
}
