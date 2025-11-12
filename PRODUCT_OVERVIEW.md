# Pangaea Kaigi - AI Meeting System

## Product Vision

A system that supports corporate decision-makers in making logical and multifaceted decisions through fast and rigorous discussions powered by multiple AI agents.

## Problem Statement

### Target Users
- Corporate decision-makers considering business strategies or important internal decisions
- Individuals struggling alone, feeling uncertain about whether their decisions are correct
- People who lack confidence that their thinking is truly thorough

### Value Proposition

1. **Fast and Rigorous Multi-Perspective Discussion**
   - Multiple AI agents contribute opinions from different viewpoints
   - High-quality discussions in a short time

2. **Logical Decision-Making Process**
   - Pure logical discussion not influenced by emotions or authority
   - All opinions are evaluated fairly

3. **Decision Recording and Knowledge Transfer**
   - Decision rationale is stored as data
   - Easy handover to successors
   - Clear explanations to subordinates

## System Overview

### MVP (Minimum Viable Product) Specifications

#### 1. Topic Input
Users enter the issues they want to resolve or decisions they need to make

#### 2. Agenda Creation by Facilitator
- **Role**: Facilitator Agent
- **Functions**:
  - Divide the input topic into multiple sub-topics
  - Determine the discussion order (create agenda)
  - Design a logical discussion flow to reach a final conclusion

Example:
```
Original Topic: Direction for new business ventures
↓
Agenda:
1. Market environment analysis
2. Confirm company strengths
3. List business candidates
4. Evaluate each candidate
5. Final business selection
```

#### 3. Automatic Agent Generation
- **Role**: Facilitator Agent
- **Functions**:
  - Automatically generate 4-6 agents with perspectives suited to the topic
  - Assign specific viewpoints and expertise to each agent
  - Examples: Financial expert, marketing expert, technical lead, customer advocate, etc.

#### 4. Discussion Process (Conducted for Each Agenda Item)

##### Phase 1: Independent Opinion Formation
- Each agent expresses their opinion without being influenced by others
- This achieves "rigor" in the meeting
- Other opinions remain hidden until all agents have shared their views

##### Phase 2: Voting to Narrow Opinions
- Each agent votes for the one opinion they consider "most logically sound"
- Opinions with 0 votes are eliminated
- Only opinions with 1 or more votes proceed to the next phase

##### Phase 3: Persuasion Process Starting from Minority
1. The supporter of the opinion with the fewest votes explains its logical superiority
2. Other agents determine if they can agree with the explanation
3. If everyone agrees → Decision made
4. If someone cannot agree → Move to the next minority opinion for persuasion
5. Repeat until a unanimous opinion emerges

##### Facilitator Intervention
- When the discussion reaches a deadlock
- Pose sharp questions to encourage deeper consideration
- Improve discussion quality and support consensus formation

#### 5. Final Output
- Agreed-upon conclusions for each agenda item
- Final answer to the original topic
- Logical decision agreed upon by all participating agents

## System Features

### Ensuring Rigor
- Independent opinion formation eliminates conformity pressure
- Reliably collects opinions from diverse perspectives

### Pursuit of Logic
- Opinions evaluated based on logical validity, not emotion or authority
- Derive the most logical conclusion through persuasion process

### Democratic Process
- All opinions are treated equally
- Minority opinions are always heard
- Aim for unanimous consensus

### Transparency and Recording
- All discussion processes are recorded
- Decision rationale is clear
- Review and verification possible after the fact

## Technology Stack

### Frontend
- Next.js 16
- React
- TypeScript
- Tailwind CSS
- Real-time chat UI (LINE-style)

### Backend
- Python 3.11+
- FastAPI
- OpenAI Responses API (GPT-4.1-mini)
- WebSocket (real-time communication)

### Future Extensions
- Database (discussion history storage)
- Authentication system
- Agent configuration customization features

## MVP Technical Specifications

### LLM Design

#### Model Used
- **OpenAI GPT-4.1-mini** for all agents
- **Responses API** (new API introduced in 2025)
- Each agent maintains independent conversation state (different `previous_response_id`)

#### Responses API Features
OpenAI's new Responses API has server-side conversation state management capabilities:

- **`store: true` parameter**: Saves conversations on OpenAI's server
- **`previous_response_id`**: Continue conversation by specifying past response ID
- Unlike the traditional Chat Completions API, no need to send entire conversation history each time
- Conversation context is maintained by passing the ID alone

#### Context Management Design Philosophy
Designed to reproduce human thought processes:

1. **Own Opinion (Internal Thinking)**
   - Each agent has its own `previous_response_id` chain
   - Conversation history saved on OpenAI server with `store: true`
   - What an agent has thought in the past remains as memory
   - This reproduces "what one has thought with one's own mind"

2. **Others' Opinions (External Information)**
   - Explicitly shared as prompts
   - Others' opinions are treated as "information coming from outside"
   - Managed as a separate context from one's own thought chain (response_id)

#### Implementation Example
```python
# Agent A's first statement
response_a1 = client.responses.create(
    model="gpt-4.1-mini",
    input="Please state your opinion on this topic",
    store=True
)

# Agent A's second statement (in response to others' opinions)
response_a2 = client.responses.create(
    model="gpt-4.1-mini",
    input=f"Please provide a counter-argument to the following opinion: {others_opinion}",
    previous_response_id=response_a1.id,
    store=True
)
```

This design enables each agent to:
- Maintain consistent thinking
- Receive others' opinions as new information
- React to them

Thus achieving human-like discussion

### Agent Generation

#### MVP Specification
- **Fully automatic generation**
  - Facilitator analyzes the topic and automatically generates 4-6 agents
  - User adjustment features planned for post-MVP

### Discussion Flow

#### Automatic Progression
- All phases progress automatically
- No user intervention such as "Next" button required
- Users observe the discussion in real-time

#### Opinion Expression Format
- **Concise and clear text format**
- Each opinion follows this recommended structure:
  ```
  Conclusion: [Brief claim]
  Rationale: [Logical reasoning]
  ```
- Not too long, capturing key points

### Persuasion Process

#### Bidirectional Discussion
- Persuader presents
- **Other agents can counter-argue**
- Persuader may change their mind after hearing counter-arguments
- This also reproduces the flow where minority convinces majority

#### Counter-argument Flow
1. Minority agent attempts persuasion
2. Other agents counter-argue or question
3. Persuader responds
4. Each agent again expresses agreement/disagreement
5. Persuader can also change their opinion if convinced by others

### Consensus Determination

#### Explicit Declaration
- Each agent explicitly declares **Yes/No**
- Facilitator only moderates, does not participate in determination
- Consensus reached when all agents say "Yes"

### UI/UX Design

#### Real-time Chat-style Display
- **LINE-style chat UI**
- Discussion flows in real-time display
- Speech bubble displayed for each agent's statement
- Users observe the meeting live

#### Display Content
- Display all agent statements
- No summarization, show full discussion
- Phase transitions also explicitly displayed

### Data Storage

#### MVP Stage
- **No database used**
- Simple configuration to focus on discussion quality
- Data retained only during session

#### Phase 2 and Beyond
- Persistent discussion history
- Search and analysis features

### Discussion Termination Conditions

#### MVP Specification
- **Continue until unanimous agreement**
- No maximum turn count or time limit
- First verify if high-quality consensus formation process works

#### Future Extensions
- Based on operational results, add termination conditions if needed
- Examples: Maximum turn count, time limit, user-forced termination, etc.

## Development Phases

### Phase 1: MVP Development
- [ ] Facilitator Agent implementation
- [ ] Automatic agenda generation feature
- [ ] Automatic participant agent generation feature
- [ ] Discussion process implementation
  - [ ] Independent opinion formation
  - [ ] Voting feature
  - [ ] Persuasion process
- [ ] Basic UI/UX

### Phase 2: Feature Extensions
- [ ] Discussion history storage and search
- [ ] User account management
- [ ] Discussion pause and resume feature
- [ ] More advanced facilitation features

### Phase 3: Enterprise Features
- [ ] Organization management features
- [ ] Permission management
- [ ] Discussion templates
- [ ] Analysis and reporting features
- [ ] Decision traceability

## Expected Benefits

1. **Improved Decision Quality**
   - More multi-perspective viewpoints
   - More logical conclusions

2. **Faster Decision Making**
   - Fast discussion by AI
   - No scheduling required

3. **Organizational Knowledge Accumulation**
   - Recording of decision-making processes
   - Knowledge transfer

4. **Enhanced Accountability**
   - Transparent decision-making process
   - Clear rationale
