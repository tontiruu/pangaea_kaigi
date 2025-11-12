# Technical Architecture

## Backend Architecture

### Directory Structure
```
backend/
├── main.py                      # FastAPI application entry point
├── config.py                    # Configuration management
├── requirements.txt             # Dependencies
├── api/                         # API endpoints
│   ├── __init__.py
│   ├── routes.py                # Route definitions
│   └── websocket.py             # WebSocket connection management
├── models/                      # Data models
│   ├── __init__.py
│   ├── agent.py                 # Agent-related models
│   ├── message.py               # Message model
│   └── discussion.py            # Discussion session model
├── services/                    # Business logic
│   ├── __init__.py
│   ├── openai_client.py         # OpenAI Responses API client
│   ├── facilitator.py           # Facilitator Agent
│   ├── agent_manager.py         # Agent generation and management
│   └── discussion_engine.py     # Discussion flow control
└── utils/                       # Utilities
    ├── __init__.py
    └── prompts.py               # Prompt templates
```

## Frontend Architecture

### Directory Structure
```
frontend/
├── app/
│   ├── page.tsx                 # Home page (topic input)
│   ├── layout.tsx
│   ├── discussion/
│   │   └── [id]/
│   │       └── page.tsx         # Discussion screen
│   └── api/
│       └── discussion/
│           └── route.ts         # API routes (as needed)
├── components/
│   ├── chat/
│   │   ├── ChatContainer.tsx    # Chat container
│   │   ├── MessageBubble.tsx    # Message bubble
│   │   ├── AgentAvatar.tsx      # Agent avatar
│   │   └── PhaseIndicator.tsx   # Phase indicator
│   ├── input/
│   │   └── TopicInput.tsx       # Topic input form
│   └── ui/                      # General UI components
├── hooks/
│   ├── useWebSocket.ts          # WebSocket management hook
│   └── useDiscussion.ts         # Discussion state management hook
├── types/
│   ├── agent.ts                 # Agent type definitions
│   ├── message.ts               # Message type definitions
│   └── discussion.ts            # Discussion type definitions
└── lib/
    └── websocket.ts             # WebSocket client
```

## Data Flow

### 1. Topic Input Flow
```
User Input (Frontend)
  ↓
POST /api/discussions
  ↓
Facilitator.create_agenda()
  ↓
Facilitator.generate_agents()
  ↓
WebSocket: agenda_created, agents_created
  ↓
Frontend: Display agenda & agents
  ↓
Discussion Engine starts
```

### 2. Discussion Flow
```
Discussion Engine
  ↓
Phase 1: Independent Opinions
  ├─ Agent A: OpenAI Responses API (store=true)
  ├─ Agent B: OpenAI Responses API (store=true)
  └─ ...
  ↓ WebSocket: agent_opinion_posted (each)
  ↓
Phase 2: Voting
  ├─ Each Agent votes
  └─ Filter opinions (≥1 vote)
  ↓ WebSocket: voting_completed
  ↓
Phase 3: Persuasion Loop
  ├─ Minority presents (previous_response_id)
  ├─ Others respond/object (previous_response_id)
  ├─ Re-vote
  └─ Repeat until consensus
  ↓ WebSocket: messages in real-time
  ↓
Consensus reached
  ↓ WebSocket: agenda_completed
  ↓
Move to next agenda
```

## Core Class Design

### Agent Class
```python
class Agent:
    id: str
    name: str
    role: str
    perspective: str
    response_id: Optional[str]  # OpenAI response_id chain

    async def generate_opinion(input: str) -> str
    async def vote(opinions: List[Opinion]) -> str
    async def respond(message: str) -> str
```

### Facilitator Class
```python
class Facilitator:
    response_id: Optional[str]

    async def create_agenda(topic: str) -> List[AgendaItem]
    async def generate_agents(topic: str, agenda: List) -> List[Agent]
    async def intervene(discussion_state: dict) -> Optional[str]
```

### DiscussionEngine Class
```python
class DiscussionEngine:
    facilitator: Facilitator
    agents: List[Agent]
    current_agenda_index: int

    async def start_discussion()
    async def run_phase_1_independent_opinions()
    async def run_phase_2_voting()
    async def run_phase_3_persuasion()
    async def check_consensus() -> bool
```

## WebSocket Event Design

### Server → Client Events

```typescript
// Discussion started
{
  type: 'discussion_started',
  data: {
    discussion_id: string,
    topic: string
  }
}

// Agenda creation completed
{
  type: 'agenda_created',
  data: {
    agenda: AgendaItem[]
  }
}

// Agent generation completed
{
  type: 'agents_created',
  data: {
    agents: Agent[]
  }
}

// Phase changed
{
  type: 'phase_changed',
  data: {
    phase: 'independent' | 'voting' | 'persuasion',
    agenda_index: number
  }
}

// Message sent
{
  type: 'message',
  data: {
    agent_id: string,
    agent_name: string,
    content: string,
    timestamp: string
  }
}

// Voting result
{
  type: 'voting_result',
  data: {
    votes: Record<string, number>
  }
}

// Agenda completed
{
  type: 'agenda_completed',
  data: {
    agenda_index: number,
    conclusion: string
  }
}

// Discussion completed
{
  type: 'discussion_completed',
  data: {
    final_conclusion: string
  }
}

// Error
{
  type: 'error',
  data: {
    message: string
  }
}
```

### Client → Server Events

```typescript
// Discussion start request
{
  type: 'start_discussion',
  data: {
    topic: string
  }
}
```

## OpenAI Responses API Integration

### Context Management Strategy

Each Agent maintains an independent `response_id` chain:

```python
# Agent's first statement
response = await client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
    store=True
)
agent.response_id = response.id

# Agent's subsequent statements
response = await client.responses.create(
    model="gpt-4.1-mini",
    input=f"Other opinions: {others_opinions}\n\nYour response: ",
    previous_response_id=agent.response_id,
    store=True
)
agent.response_id = response.id  # Update
```

### Error Handling
- Rate limit handling: Exponential backoff
- API failures: Retry logic
- Timeouts: Appropriate configuration

## Security Considerations

### API Key Management
- Managed via environment variables (`.env`)
- API keys used only in backend
- Never exposed to frontend

### WebSocket Authentication
- MVP stage: Simple connection
- Phase 2: Token-based authentication

## Performance Optimization

### Parallel Processing
- Phase 1 independent opinions: All agents execute in parallel
- Voting: All agents execute in parallel

### Streaming
- Leverage OpenAI API streaming responses
- Real-time transmission to frontend

## Development Approach

### Phase 1: Core Feature Implementation
1. OpenAI Responses API client
2. Basic Agent class
3. Basic Facilitator functionality
4. Simple discussion flow

### Phase 2: WebSocket Integration
5. WebSocket connection management
6. Real-time communication

### Phase 3: Frontend
7. Chat UI
8. WebSocket connection
9. State management

### Phase 4: Integration Testing
10. End-to-end testing
11. Debugging and optimization
