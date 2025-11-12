# Pangaea Kaigi

## **Alignment with Y Combinator RFS**

Our "LLM Meeting Agent" is a B2B SaaS that directly addresses multiple RFS themes Y Combinator is seeking.

### **1. Infrastructure for Multi-Agent Systems**

Our service is a multi-agent infrastructure specifically designed for "strategic decision-making." The Facilitator Agent handles "monitoring" and "dynamic prompt generation," while our proprietary consensus-building algorithm guides the AI agent fleet's output toward "reliable" conclusions.

### **2. Automating Complex, Legacy Workflows**

We target the most complex, person-dependent, and legacy workflow in any company: "executive decision-making." Through AI-driven MECE (Mutually Exclusive, Collectively Exhaustive) issue generation and high-speed debate, we replace traditional "intuition and experience"-based processes with an AI-native workflow.

### **3. AI for Governance, Compliance & Audit**

The "black box" nature of AI is a key governance challenge. Our service "logs the entire discussion process" leading to a decision. This makes the thought process of both AI (and humans) fully "auditable," fulfilling a high level of "accountability" to stakeholders, shareholders, and auditors.

フロントエンド（Next.js + React）とバックエンド（FastAPI）を含むフルスタックアプリケーション。

## 構成

```
pangaea_kaigi/
├── backend/          # FastAPI バックエンド
│   ├── main.py       # FastAPIアプリケーション
│   ├── config.py     # 設定管理
│   ├── requirements.txt
│   ├── .env.example  # 環境変数のテンプレート
│   └── .gitignore
├── frontend/         # Next.js フロントエンド
├── Makefile          # プロジェクト管理用Makefile
└── README.md
```

## セットアップ

### 1. 環境変数の設定

バックエンドの環境変数を設定します：

```bash
cd backend
cp .env.example .env
```

必要に応じて`.env`ファイルを編集してください。

### 2. 依存関係のインストール

```bash
make install
```

または個別に：

```bash
make install-backend  # バックエンドの依存関係
make install-frontend # フロントエンドの依存関係
```

## 起動方法

### 両方を同時に起動

```bash
make start
```

このコマンドで以下が起動します：

- バックエンド: http://localhost:8000
- フロントエンド: http://localhost:3000

### 個別に起動

```bash
make dev-backend   # バックエンドのみ
make dev-frontend  # フロントエンドのみ
```

## 停止方法

```bash
make stop
```

## API エンドポイント

バックエンドは以下のエンドポイントを提供します：

- `GET /` - ルートエンドポイント
- `GET /api/health` - ヘルスチェック

## 技術スタック

### フロントエンド

- Next.js 16
- React
- TypeScript
- Tailwind CSS

### バックエンド

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic Settings（環境変数管理）

## 環境変数

バックエンドで使用可能な環境変数：

### 基本設定

| 変数名         | 説明                              | デフォルト値                                  |
| -------------- | --------------------------------- | --------------------------------------------- |
| `DEBUG`        | デバッグモード                    | `True`                                        |
| `APP_NAME`     | アプリケーション名                | `Pangaea Kaigi API`                           |
| `API_VERSION`  | API バージョン                    | `0.1.0`                                       |
| `HOST`         | サーバーホスト                    | `0.0.0.0`                                     |
| `PORT`         | サーバーポート                    | `8000`                                        |
| `CORS_ORIGINS` | CORS 許可オリジン（カンマ区切り） | `http://localhost:3000,http://127.0.0.1:3000` |

### AI 設定

| 変数名           | 説明            | 必須 |
| ---------------- | --------------- | ---- |
| `OPENAI_API_KEY` | OpenAI API キー | ✓    |

### MCP 統合設定（Dedalus Labs）

会議の背景知識を取得するための設定です。

| 変数名                     | 説明                                              | 必須                   |
| -------------------------- | ------------------------------------------------- | ---------------------- |
| `DEDALUS_API_KEY`          | [Dedalus Labs](https://dedaluslabs.ai)の API キー | ✓                      |
| `ENABLE_CONTEXT_RETRIEVAL` | 背景知識取得の有効化                              | ✗ (デフォルト: `True`) |

### Notion 統合（オプション）

Notion から関連ドキュメントを検索します。

| 変数名         | 説明                |
| -------------- | ------------------- |
| `NOTION_TOKEN` | Notion 統合トークン |

**取得方法:**

1. [Notion Integrations](https://www.notion.so/my-integrations)にアクセス
2. 「New integration」をクリック
3. 統合を作成し、トークンを取得
4. 検索したいページに統合を招待

### Slack 統合（オプション）

Slack から過去の議論を検索します。

| 変数名            | 説明                            |
| ----------------- | ------------------------------- |
| `SLACK_BOT_TOKEN` | Slack Bot Token (xoxb-で始まる) |
| `SLACK_TEAM_ID`   | Slack Team ID                   |

**取得方法:**

1. [Slack API](https://api.slack.com/apps)にアクセス
2. アプリを作成
3. Bot Token Scopes に必要な権限を追加（`search:read`, `channels:history`, `groups:history`など）
4. アプリをワークスペースにインストール

### Atlassian 統合（オプション）

Jira と Confluence から関連情報を検索します。

| 変数名                | 説明                                                  |
| --------------------- | ----------------------------------------------------- |
| `ATLASSIAN_EMAIL`     | Atlassian アカウントのメールアドレス                  |
| `ATLASSIAN_API_TOKEN` | Atlassian API トークン                                |
| `ATLASSIAN_DOMAIN`    | Atlassian ドメイン（例: `your-domain.atlassian.net`） |

**取得方法:**

1. [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)にアクセス
2. 「Create API token」をクリック
3. トークンを取得

## MCP 統合について

このプロジェクトは[Dedalus Labs](https://dedaluslabs.ai)を使用して、複数の MCP サービス（Notion、Slack、Atlassian など）から統一的に情報を取得します。

### 仕組み

1. 会議トピックが与えられると、関連キーワードを抽出
2. Dedalus Labs 経由で各 MCP サービスに問い合わせ
3. 取得した背景知識を AI エージェントに提供
4. より文脈を理解した議論が可能に

### 設定例

最小限の設定（MCP 統合なし）:

```bash
OPENAI_API_KEY=sk-...
DEDALUS_API_KEY=your-key
ENABLE_CONTEXT_RETRIEVAL=False
```

Notion 統合のみ有効化:

```bash
OPENAI_API_KEY=sk-...
DEDALUS_API_KEY=your-key
NOTION_TOKEN=secret_...
```

すべての統合を有効化:

```bash
OPENAI_API_KEY=sk-...
DEDALUS_API_KEY=your-key
NOTION_TOKEN=secret_...
SLACK_BOT_TOKEN=xoxb-...
SLACK_TEAM_ID=T...
ATLASSIAN_EMAIL=you@example.com
ATLASSIAN_API_TOKEN=ATATT...
ATLASSIAN_DOMAIN=your-domain.atlassian.net
```
