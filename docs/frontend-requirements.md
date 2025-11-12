# フロントエンド要件定義書

## 概要

Pangaea Kaigiのフロントエンドに、背景知識（コンテキスト）取得・表示機能を追加します。

## 目的

- 議論開始前に関連する背景知識を確認できるようにする
- Notion/Slack/Atlassianから取得した情報を視覚的にわかりやすく表示
- どのような背景情報が議論に活用されているかを透明化

## 新規追加画面・コンポーネント

### 1. 背景知識取得パネル（Context Panel）

**配置場所:** 議論開始画面（トピック入力画面）

**機能:**
- 議論トピック入力後、「背景知識を取得」ボタンを表示
- ボタンクリックでバックエンドAPI `/api/context/retrieve` を呼び出し
- 取得中はローディングスピナーを表示
- 取得完了後、結果を一覧表示

**UI要素:**
```
┌─────────────────────────────────────────┐
│ 議論トピック                               │
│ ┌─────────────────────────────────────┐ │
│ │ 新機能の優先順位付け                   │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ [🔍 背景知識を取得]  [▶ 議論を開始]      │
└─────────────────────────────────────────┘

取得後 ↓

┌─────────────────────────────────────────┐
│ 背景知識（10件）                          │
│ ┌─────────────────────────────────────┐ │
│ │ [Notion] プロダクト開発ロードマップ     │ │
│ │ 過去3ヶ月のスプリントで...            │ │
│ │ 📎 https://notion.so/...             │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ [Slack] #engineering チャンネル        │ │
│ │ @tanaka: 新機能のデプロイについて...   │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ [Jira] PROJ-123: ユーザー検索機能     │ │
│ │ ステータス: 進行中...                 │ │
│ │ 📎 https://jira.example.com/...      │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ [▶ この背景知識を使って議論を開始]       │
└─────────────────────────────────────────┘
```

### 2. コンテキストカード（Context Card）

**目的:** 個別の背景知識を表示

**表示項目:**
- ソースアイコン（Notion/Slack/Atlassian）
- タイトル
- 内容プレビュー（最初の200文字程度）
- URL（リンク）
- 展開/折りたたみボタン

**インタラクション:**
- カードクリックで詳細を展開
- URLクリックで外部リンクを開く（新しいタブ）
- ソースアイコンで色分け
  - Notion: 黒/白
  - Slack: 紫
  - Atlassian: 青

### 3. ソース設定状態表示（Source Status Indicator）

**配置場所:** 設定画面またはヘッダー

**機能:**
- どのMCPサービスが有効化されているか表示
- `/api/context/sources` を呼び出して状態を取得

**UI要素:**
```
┌─────────────────────────────────────────┐
│ 背景知識連携設定                          │
│                                          │
│ ✅ Notion    （設定済み）                │
│ ❌ Slack     （未設定）                  │
│ ✅ Atlassian （設定済み）                │
│                                          │
│ ⚙️ Dedalus Labs API: 設定済み           │
└─────────────────────────────────────────┘
```

### 4. 議論中の背景知識参照パネル

**配置場所:** 議論画面のサイドバー（オプション）

**機能:**
- 議論中も取得した背景知識を参照可能
- 折りたたみ/展開可能
- スクロール可能

## API連携

### 背景知識取得API

**エンドポイント:** `POST /api/context/retrieve`

**リクエスト:**
```typescript
interface ContextRetrievalRequest {
  topic: string;
  keywords?: string[];
}
```

**レスポンス:**
```typescript
interface ContextRetrievalResponse {
  topic: string;
  keywords: string[];
  count: number;
  contexts: ContextItem[];
}

interface ContextItem {
  source: 'notion' | 'slack' | 'atlassian';
  title: string;
  content: string;
  url: string | null;
  metadata: {
    section?: string;
    [key: string]: any;
  } | null;
}
```

### ソース状態取得API

**エンドポイント:** `GET /api/context/sources`

**レスポンス:**
```typescript
interface SourcesResponse {
  sources: {
    name: string;
    enabled: boolean;
    description: string;
  }[];
  dedalus_configured: boolean;
  context_retrieval_enabled: boolean;
}
```

## 実装の優先順位

### Phase 1: 基本機能（MVP）
1. 背景知識取得ボタンの追加
2. APIコール実装
3. 基本的なコンテキストカード表示
4. ローディング状態の表示

### Phase 2: UX改善
1. カードの展開/折りたたみ
2. ソースアイコンと色分け
3. エラーハンドリングとメッセージ表示
4. レスポンシブデザイン対応

### Phase 3: 高度な機能
1. ソース設定状態表示
2. 議論中の背景知識参照パネル
3. キーワードハイライト
4. フィルタリング機能（ソース別）

## 技術スタック

- **フレームワーク:** Next.js 16 + React
- **言語:** TypeScript
- **スタイリング:** Tailwind CSS
- **状態管理:** React Hooks（useState, useEffect）
- **APIクライアント:** fetch または axios

## 必要なカスタムフック

### useContextRetrieval

```typescript
function useContextRetrieval() {
  const [contexts, setContexts] = useState<ContextItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const retrieveContext = async (topic: string, keywords?: string[]) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/context/retrieve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, keywords }),
      });
      const data = await response.json();
      setContexts(data.contexts);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { contexts, loading, error, retrieveContext };
}
```

### useContextSources

```typescript
function useContextSources() {
  const [sources, setSources] = useState<SourceInfo[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchSources = async () => {
      setLoading(true);
      try {
        const response = await fetch('/api/context/sources');
        const data = await response.json();
        setSources(data.sources);
      } catch (err) {
        console.error('Failed to fetch sources:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchSources();
  }, []);

  return { sources, loading };
}
```

## コンポーネント構成

```
app/
├── discussion/
│   ├── page.tsx                    # 既存の議論画面
│   └── components/
│       ├── ContextPanel.tsx        # 新規: 背景知識パネル
│       ├── ContextCard.tsx         # 新規: コンテキストカード
│       ├── ContextSidebar.tsx      # 新規: サイドバー（議論中）
│       └── SourceStatusBadge.tsx   # 新規: ソース状態表示
└── settings/
    └── components/
        └── SourcesConfig.tsx        # 新規: ソース設定表示
```

## デザインガイドライン

### カラーパレット

```css
/* ソース別カラー */
--notion-color: #000000;
--slack-color: #4A154B;
--atlassian-color: #0052CC;

/* 状態カラー */
--loading-color: #94A3B8;
--success-color: #10B981;
--error-color: #EF4444;
```

### スペーシング

- カード間のマージン: `16px`
- パネル内のパディング: `24px`
- カードのパディング: `16px`

### タイポグラフィ

- カードタイトル: `font-semibold text-lg`
- カード本文: `text-sm text-gray-700`
- メタ情報: `text-xs text-gray-500`

## エラーハンドリング

### 表示するエラーメッセージ

1. **API接続エラー:**
   ```
   背景知識の取得に失敗しました。
   ネットワーク接続を確認してください。
   ```

2. **データ取得エラー:**
   ```
   背景知識を取得できませんでした。
   しばらく待ってから再試行してください。
   ```

3. **設定不足エラー:**
   ```
   MCPサービスが設定されていません。
   設定画面から連携を有効化してください。
   ```

## アクセシビリティ要件

- キーボードナビゲーション対応
- スクリーンリーダー対応（aria-label追加）
- カラーコントラスト比 4.5:1 以上
- フォーカスインジケーター表示

## パフォーマンス要件

- 背景知識取得APIのレスポンス時間: 3秒以内
- カードレンダリング: 100件まで対応
- 仮想スクロール実装（100件以上の場合）

## テスト要件

### ユニットテスト
- カスタムフックのテスト
- 個別コンポーネントのレンダリングテスト

### インテグレーションテスト
- API連携のテスト（モック使用）
- エラーハンドリングのテスト

### E2Eテスト
- 背景知識取得フローのテスト
- 議論開始までの一連の流れ

## 実装時の注意点

1. **モックデータ対応:**
   - 現在バックエンドはモックデータを返すため、実際のMCP統合前でも動作確認可能
   - 実装時は `use_mock=True` が前提

2. **将来の拡張性:**
   - 新しいMCPサービス（GitHub、Linear等）追加に対応できる設計
   - ソースタイプは型で管理（`type Source = 'notion' | 'slack' | 'atlassian'`）

3. **レスポンシブ対応:**
   - モバイル: 1カラム、折りたたみ表示
   - タブレット: 2カラム
   - デスクトップ: サイドバー表示

## 参考リンク

- [バックエンドAPI実装](/backend/api/routes.py)
- [MCP統合ガイド](/docs/mcp-integration.md)
- [モックデータ](/backend/mock_data.txt)
