/**
 * 議論セッション型定義
 */

export enum DiscussionPhase {
  INITIALIZING = "initializing",
  AGENDA_CREATION = "agenda_creation",
  AGENT_GENERATION = "agent_generation",
  INDEPENDENT_OPINIONS = "independent_opinions",
  VOTING = "voting",
  PERSUASION = "persuasion",
  COMPLETED = "completed",
}

export interface AgendaItem {
  id: string;
  title: string;
  description: string;
  order: number;
  conclusion?: string;
}

export interface DiscussionSession {
  id: string;
  topic: string;
  agenda: AgendaItem[];
  current_agenda_index: number;
  phase: DiscussionPhase;
  created_at: string;
  final_conclusion?: string;
}
