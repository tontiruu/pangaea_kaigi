# Technical Architecture

## バックエンドアーキテクチャ

### ディレクトリ構造
```
backend/
├── main.py                      # FastAPI アプリケーションのエントリーポイント
├── config.py                    # 設定管理
├── requirements.txt             # 依存関係
├── api/                         # APIエンドポイント
│   ├── __init__.py
│   ├── routes.py                # ルート定義
│   └── websocket.py             # WebSocket接続管理
├── models/                      # データモデル
│   ├── __init__.py
│   ├── agent.py                 # Agent関連のモデル
│   ├── message.py               # メッセージモデル
│   └── discussion.py            # 議論セッションモデル
├── services/                    # ビジネスロジック
│   ├── __init__.py
│   ├── openai_client.py         # OpenAI Responses API クライアント
│   ├── facilitator.py           # ファシリテーターAgent
│   ├── agent_manager.py         # Agent生成・管理
│   └── discussion_engine.py     # 議論フロー制御
└── utils/                       # ユーティリティ
    ├── __init__.py
    └── prompts.py               # プロンプトテンプレート
```

## フロントエンドアーキテクチャ

### ディレクトリ構造
```
frontend/
├── app/
│   ├── page.tsx                 # ホームページ（議題入力）
│   ├── layout.tsx
│   ├── discussion/
│   │   └── [id]/
│   │       └── page.tsx         # 議論画面
│   └── api/
│       └── discussion/
│           └── route.ts         # API routes（必要に応じて）
├── components/
│   ├── chat/
│   │   ├── ChatContainer.tsx    # チャットコンテナ
│   │   ├── MessageBubble.tsx    # メッセージ吹き出し
│   │   ├── AgentAvatar.tsx      # Agent アバター
│   │   └── PhaseIndicator.tsx   # フェーズ表示
│   ├── input/
│   │   └── TopicInput.tsx       # 議題入力フォーム
│   └── ui/                      # 汎用UIコンポーネント
├── hooks/
│   ├── useWebSocket.ts          # WebSocket管理フック
│   └── useDiscussion.ts         # 議論状態管理フック
├── types/
│   ├── agent.ts                 # Agent型定義
│   ├── message.ts               # メッセージ型定義
│   └── discussion.ts            # 議論型定義
└── lib/
    └── websocket.ts             # WebSocketクライアント
```

## データフロー

### 1. 議題入力フロー
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

### 2. 議論フロー
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

## コアクラス設計

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

## WebSocketイベント設計

### Server → Client イベント

```typescript
// 議論開始
{
  type: 'discussion_started',
  data: {
    discussion_id: string,
    topic: string
  }
}

// アジェンダ作成完了
{
  type: 'agenda_created',
  data: {
    agenda: AgendaItem[]
  }
}

// Agent生成完了
{
  type: 'agents_created',
  data: {
    agents: Agent[]
  }
}

// フェーズ変更
{
  type: 'phase_changed',
  data: {
    phase: 'independent' | 'voting' | 'persuasion',
    agenda_index: number
  }
}

// メッセージ送信
{
  type: 'message',
  data: {
    agent_id: string,
    agent_name: string,
    content: string,
    timestamp: string
  }
}

// 投票結果
{
  type: 'voting_result',
  data: {
    votes: Record<string, number>
  }
}

// アジェンダ完了
{
  type: 'agenda_completed',
  data: {
    agenda_index: number,
    conclusion: string
  }
}

// 議論完了
{
  type: 'discussion_completed',
  data: {
    final_conclusion: string
  }
}

// エラー
{
  type: 'error',
  data: {
    message: string
  }
}
```

### Client → Server イベント

```typescript
// 議論開始リクエスト
{
  type: 'start_discussion',
  data: {
    topic: string
  }
}
```

## OpenAI Responses API統合

### コンテキスト管理戦略

各Agentは独立した`response_id`チェーンを保持：

```python
# Agent初回発言
response = await client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
    store=True
)
agent.response_id = response.id

# Agent後続発言
response = await client.responses.create(
    model="gpt-4.1-mini",
    input=f"他の意見: {others_opinions}\n\nあなたの反応: ",
    previous_response_id=agent.response_id,
    store=True
)
agent.response_id = response.id  # 更新
```

### エラーハンドリング
- Rate limit対応: Exponential backoff
- API障害時: リトライロジック
- タイムアウト: 適切な設定

## セキュリティ考慮事項

### API Key管理
- 環境変数での管理（`.env`）
- バックエンドでのみAPI Key使用
- フロントエンドには絶対に露出させない

### WebSocket認証
- MVP段階: シンプルな接続
- Phase 2: トークンベース認証

## パフォーマンス最適化

### 並列処理
- Phase 1の独立意見出し: 全Agent並列実行
- 投票: 全Agent並列実行

### ストリーミング
- OpenAI APIのストリーミングレスポンスを活用
- リアルタイムでフロントエンドに送信

## 開発の進め方

### Phase 1: コア機能実装
1. OpenAI Responses API クライアント
2. Agent基本クラス
3. Facilitator基本機能
4. シンプルな議論フロー

### Phase 2: WebSocket統合
5. WebSocket接続管理
6. リアルタイム通信

### Phase 3: フロントエンド
7. チャットUI
8. WebSocket接続
9. 状態管理

### Phase 4: 統合テスト
10. エンドツーエンドテスト
11. デバッグ・最適化
