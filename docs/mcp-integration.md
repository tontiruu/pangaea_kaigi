# MCP統合ガイド

このドキュメントでは、Dedalus Labsを使用したMCP（Model Context Protocol）統合について詳しく説明します。

## 概要

Pangaea KaigiはDedalus Labsを使用して、複数の外部サービス（Notion、Slack、Atlassianなど）から背景知識を取得し、AIエージェントによる会議の質を向上させます。

## アーキテクチャ

```
議論トピック
    ↓
キーワード抽出
    ↓
┌─────────────────────────────┐
│   Dedalus Labs MCP Hub      │
├─────────────────────────────┤
│  ┌─────┐  ┌─────┐  ┌─────┐ │
│  │Notion│ │Slack│ │Jira │ │
│  └─────┘  └─────┘  └─────┘ │
└─────────────────────────────┘
    ↓
背景知識の構造化
    ↓
AIエージェントへ提供
    ↓
文脈を理解した議論
```

## セットアップ

### 1. Dedalus Labs APIキーの取得

1. [Dedalus Labs](https://dedaluslabs.ai)にアクセス
2. アカウントを作成
3. APIキーを取得
4. `.env`ファイルに設定:
   ```bash
   DEDALUS_API_KEY=your-api-key-here
   ```

### 2. MCPサービスの設定

#### Notion統合

**必要な権限:**
- Read content
- Search

**設定手順:**

1. [Notion Integrations](https://www.notion.so/my-integrations)にアクセス
2. 「New integration」をクリック
3. 統合名を入力（例: "Pangaea Kaigi"）
4. "Read content"と"Search"の権限を有効化
5. トークンをコピー
6. `.env`に追加:
   ```bash
   NOTION_TOKEN=secret_xxxxxxxxxxxxx
   ```
7. Notionで検索対象のページを開く
8. 「...」メニュー → 「Connections」→ 作成した統合を選択

#### Slack統合

**必要な権限:**
- `search:read`
- `channels:history`
- `groups:history`
- `channels:read`

**設定手順:**

1. [Slack API](https://api.slack.com/apps)にアクセス
2. 「Create New App」→ 「From scratch」
3. アプリ名とワークスペースを選択
4. 「OAuth & Permissions」に移動
5. 「Scopes」セクションで以下を追加:
   - `search:read`
   - `channels:history`
   - `groups:history`
   - `channels:read`
6. 「Install to Workspace」をクリック
7. Bot User OAuth Tokenをコピー（`xoxb-`で始まる）
8. Team IDを取得（ワークスペースURLから）
9. `.env`に追加:
   ```bash
   SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxx
   SLACK_TEAM_ID=Txxxxxxxxxx
   ```

#### Atlassian（Jira/Confluence）統合

**設定手順:**

1. [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)にアクセス
2. 「Create API token」をクリック
3. トークン名を入力（例: "Pangaea Kaigi"）
4. トークンをコピー
5. `.env`に追加:
   ```bash
   ATLASSIAN_EMAIL=your-email@example.com
   ATLASSIAN_API_TOKEN=ATATTxxxxxxxxxxxxx
   ATLASSIAN_DOMAIN=your-company.atlassian.net
   ```

## 使い方

### 基本的な使用

MCP統合が設定されている場合、議論開始時に自動的に背景知識が取得されます:

```python
# backend/main.py での使用例
from services.discussion_engine import DiscussionEngine

# 議論を開始
session = await discussion_engine.start_discussion(
    topic="新機能の優先順位付け"
)

# 自動的に以下が実行されます:
# 1. トピックからキーワード抽出
# 2. Notion/Slack/Atlassianから関連情報を検索
# 3. 取得した情報をAIエージェントに提供
# 4. 文脈を理解した議論を開始
```

### 取得される情報の例

#### Notionから:
- プロジェクトドキュメント
- 過去の決定事項
- 技術仕様書
- ロードマップ

#### Slackから:
- 過去の議論スレッド
- チャンネルでの意思決定
- 関連する会話の履歴

#### Atlassianから:
- 関連するJiraチケット
- Confluenceの技術ドキュメント
- プロジェクトの要件定義

## カスタマイズ

### コンテキスト取得の無効化

特定の議論でMCP統合を使いたくない場合:

```bash
# .envで設定
ENABLE_CONTEXT_RETRIEVAL=False
```

### 特定のサービスのみ使用

例: Notionのみ使用し、SlackとAtlassianは無効化

```bash
DEDALUS_API_KEY=your-key
NOTION_TOKEN=secret_xxx

# 以下をコメントアウトまたは削除
# SLACK_BOT_TOKEN=...
# ATLASSIAN_API_TOKEN=...
```

## トラブルシューティング

### Dedalus Labs APIエラー

```
Error: Dedalus API key is invalid
```

**解決方法:**
- APIキーが正しいか確認
- [Dedalus Labs](https://dedaluslabs.ai)でアカウントステータスを確認

### Notion統合エラー

```
Error retrieving from Notion: 401 Unauthorized
```

**解決方法:**
1. トークンが有効か確認
2. Notionページに統合が招待されているか確認
3. 統合の権限設定を確認

### Slack統合エラー

```
Error retrieving from Slack: missing_scope
```

**解決方法:**
1. 必要なスコープがすべて追加されているか確認
2. アプリを再インストール
3. Bot Tokenが正しいか確認

### 取得できる情報が少ない

**考えられる原因:**
- キーワード抽出が適切でない
- 検索対象のサービスに関連情報が少ない
- 統合の権限が不足している

**改善方法:**
1. より具体的な議論トピックを設定
2. 事前にNotion/Slackに関連情報を追加
3. 統合の権限を見直す

## セキュリティとプライバシー

### データの取り扱い

- 取得した情報はセッション内でのみ使用
- 外部に保存されません（Dedalus Labs経由でのみ処理）
- APIキーは環境変数で管理

### 推奨事項

1. APIキーを.gitignoreに追加（すでに設定済み）
2. 本番環境では環境変数を使用
3. 最小権限の原則に従う
4. 定期的にAPIトークンをローテーション

## パフォーマンス

### レスポンス時間

- Notion: ~2-5秒
- Slack: ~3-7秒
- Atlassian: ~2-4秒

複数のサービスを並列に呼び出すため、合計時間は最も遅いサービスに依存します。

### 最適化のヒント

1. 必要なサービスのみ有効化
2. Notionページを適切に整理
3. Slackチャンネルを整理
4. 議論トピックを明確にする

## 高度な使用例

### カスタムMCPサーバーの追加

`backend/services/context_retriever.py`を編集して、新しいMCPサービスを追加できます:

```python
async def _retrieve_from_custom_service(
    self, topic: str, keywords: List[str]
) -> List[ContextItem]:
    """カスタムサービスから情報を取得"""
    try:
        response = await self.dedalus_client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[...],
            tools=[{
                "type": "mcp",
                "server": "custom-server-name",
                "config": {
                    # カスタム設定
                }
            }]
        )
        # レスポンスをパース
        return contexts
    except Exception as e:
        logger.error(f"Error: {e}")
        return []
```

## 参考リンク

- [Dedalus Labs公式ドキュメント](https://docs.dedaluslabs.ai)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Notion API](https://developers.notion.com/)
- [Slack API](https://api.slack.com/)
- [Atlassian API](https://developer.atlassian.com/)
