# MCP連携設定画面 - フロントエンド要件定義書

## 概要

Notion、Slack、Atlassianとの連携設定を管理する設定画面をフロントエンドに実装します。
ユーザーが各サービスのAPIトークンを設定・管理できるようにします。

## 目的

- ユーザーが自分で各MCPサービスとの連携を設定できるようにする
- 設定状態を視覚的に確認できるようにする
- トークンの取得方法をガイドする
- セキュリティを考慮した実装

## 画面構成

### 1. 設定画面（Settings Page）

**ルート:** `/settings` または `/settings/integrations`

**レイアウト:**
```
┌────────────────────────────────────────────────────────┐
│ ← 戻る          MCP連携設定                             │
├────────────────────────────────────────────────────────┤
│                                                         │
│  MCP連携について                                        │
│  Notion、Slack、Atlassianから会議の背景知識を自動取得  │
│  できます。各サービスのトークンを設定してください。      │
│                                                         │
│  [詳しく見る →]                                         │
│                                                         │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Dedalus Labs API設定                                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ ⚙️ Dedalus Labs API                              │  │
│  │                                                   │  │
│  │ APIキー *                                         │  │
│  │ ┌───────────────────────────────────┐ [👁表示]   │  │
│  │ │ •••••••••••••••••••••••••••••••   │           │  │
│  │ └───────────────────────────────────┘           │  │
│  │                                                   │  │
│  │ ステータス: ✅ 接続済み                          │  │
│  │                                                   │  │
│  │ [取得方法を見る]  [接続テスト]  [保存]          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
├────────────────────────────────────────────────────────┤
│                                                         │
│  連携サービス                                           │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 📓 Notion                              [有効化]   │  │
│  │                                                   │  │
│  │ 統合トークン                                      │  │
│  │ ┌───────────────────────────────────┐ [👁表示]   │  │
│  │ │                                   │           │  │
│  │ └───────────────────────────────────┘           │  │
│  │                                                   │  │
│  │ ステータス: ❌ 未設定                            │  │
│  │                                                   │  │
│  │ [取得方法を見る]  [接続テスト]  [保存]          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 💬 Slack                            ✅ 有効      │  │
│  │                                                   │  │
│  │ Bot Token                                        │  │
│  │ ┌───────────────────────────────────┐ [👁表示]   │  │
│  │ │ xoxb-••••••••••••••••••••••••••   │           │  │
│  │ └───────────────────────────────────┘           │  │
│  │                                                   │  │
│  │ Team ID                                          │  │
│  │ ┌───────────────────────────────────┐           │  │
│  │ │ T0123456789                       │           │  │
│  │ └───────────────────────────────────┘           │  │
│  │                                                   │  │
│  │ ステータス: ✅ 接続済み                          │  │
│  │ 最終確認: 2025-01-12 14:30                       │  │
│  │                                                   │  │
│  │ [取得方法を見る]  [接続テスト]  [削除]          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 🔷 Atlassian (Jira/Confluence)      [有効化]    │  │
│  │                                                   │  │
│  │ メールアドレス                                    │  │
│  │ ┌───────────────────────────────────┐           │  │
│  │ │ you@example.com                   │           │  │
│  │ └───────────────────────────────────┘           │  │
│  │                                                   │  │
│  │ API Token                                        │  │
│  │ ┌───────────────────────────────────┐ [👁表示]   │  │
│  │ │                                   │           │  │
│  │ └───────────────────────────────────┘           │  │
│  │                                                   │  │
│  │ ドメイン                                         │  │
│  │ ┌───────────────────────────────────┐           │  │
│  │ │ your-company.atlassian.net        │           │  │
│  │ └───────────────────────────────────┘           │  │
│  │                                                   │  │
│  │ ステータス: ❌ 未設定                            │  │
│  │                                                   │  │
│  │ [取得方法を見る]  [接続テスト]  [保存]          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### 2. トークン取得ガイドモーダル

各サービスの「取得方法を見る」ボタンをクリックすると表示されるモーダル。

**Notionの例:**
```
┌────────────────────────────────────────────┐
│ Notion統合トークンの取得方法          [×]  │
├────────────────────────────────────────────┤
│                                             │
│ 1. Notion Integrationsにアクセス           │
│    🔗 https://notion.so/my-integrations    │
│    [リンクを開く]                          │
│                                             │
│ 2. 「New integration」をクリック           │
│    📸 [スクリーンショット]                 │
│                                             │
│ 3. 統合名を入力（例: "Pangaea Kaigi"）    │
│                                             │
│ 4. 必要な権限を選択:                       │
│    ☑ Read content                         │
│    ☑ Search                               │
│                                             │
│ 5. トークンをコピー                        │
│    トークンは secret_ で始まります         │
│                                             │
│ 6. Notionで検索対象のページを開く          │
│                                             │
│ 7. 「...」メニュー → 「Connections」      │
│    → 作成した統合を選択                    │
│                                             │
│                                  [閉じる]  │
└────────────────────────────────────────────┘
```

### 3. 接続テストダイアログ

「接続テスト」ボタンをクリックすると実行され、結果をモーダルで表示。

**成功時:**
```
┌────────────────────────────────────┐
│ ✅ Slack接続テスト成功         [×] │
├────────────────────────────────────┤
│                                     │
│ Slackとの接続に成功しました！       │
│                                     │
│ 検証内容:                          │
│ • Bot Token: 有効                  │
│ • Team ID: 正常                    │
│ • アクセス権限: OK                 │
│                                     │
│               [OK]                  │
└────────────────────────────────────┘
```

**失敗時:**
```
┌────────────────────────────────────┐
│ ❌ Notion接続テスト失敗        [×] │
├────────────────────────────────────┤
│                                     │
│ Notionとの接続に失敗しました        │
│                                     │
│ エラー内容:                        │
│ 401 Unauthorized                   │
│                                     │
│ 考えられる原因:                    │
│ • トークンが無効です               │
│ • Notionページに統合が招待されて   │
│   いません                         │
│                                     │
│      [再試行]  [キャンセル]        │
└────────────────────────────────────┘
```

### 4. 設定状態の概要表示（ヘッダー or ダッシュボード）

**ヘッダーバッジ例:**
```
┌──────────────────────────────────────┐
│ Pangaea Kaigi    [🔗 2/3]  [設定]   │
└──────────────────────────────────────┘
         ↑
    連携数表示
```

**ダッシュボードカード例:**
```
┌──────────────────────────────────┐
│ MCP連携設定                       │
│                                   │
│ ✅ Notion                         │
│ ✅ Slack                          │
│ ❌ Atlassian                      │
│                                   │
│ [設定を管理 →]                   │
└──────────────────────────────────┘
```

## 機能要件

### 1. トークン管理

#### 保存機能
- **ローカル保存（推奨）:** localStorage または IndexedDB
- **バックエンド保存（オプション）:** APIエンドポイント経由
- トークンは暗号化して保存（Base64エンコード程度でも可）

#### 表示/非表示切り替え
- デフォルトはマスク表示（`••••••••`）
- 👁アイコンクリックで表示/非表示を切り替え
- セキュリティ警告の表示（公共の場では注意）

#### バリデーション
- **Dedalus API Key:** 必須、空白不可
- **Notion Token:** `secret_` で始まる文字列
- **Slack Bot Token:** `xoxb-` で始まる文字列
- **Slack Team ID:** `T` で始まる英数字
- **Atlassian Email:** 有効なメールアドレス形式
- **Atlassian Token:** `ATATT` で始まる文字列
- **Atlassian Domain:** `.atlassian.net` で終わる

### 2. 接続テスト機能

各サービスに対して接続テストを実行できる機能。

**APIエンドポイント（新規作成が必要）:**
```
POST /api/context/test-connection
```

**リクエスト:**
```typescript
interface TestConnectionRequest {
  service: 'dedalus' | 'notion' | 'slack' | 'atlassian';
  credentials: {
    // Dedalusの場合
    dedalus_api_key?: string;

    // Notionの場合
    notion_token?: string;

    // Slackの場合
    slack_bot_token?: string;
    slack_team_id?: string;

    // Atlassianの場合
    atlassian_email?: string;
    atlassian_api_token?: string;
    atlassian_domain?: string;
  };
}
```

**レスポンス:**
```typescript
interface TestConnectionResponse {
  success: boolean;
  service: string;
  message: string;
  details?: {
    checked_at: string;
    permissions?: string[];
    workspace_name?: string; // Slackの場合
  };
  error?: {
    code: string;
    message: string;
    suggestions: string[];
  };
}
```

### 3. 有効化/無効化トグル

- 各サービスごとに有効/無効を切り替え
- トグルスイッチまたはチェックボックス
- 無効化時もトークンは保持（再有効化が簡単）

### 4. ステータス表示

各サービスの状態を視覚的に表示:

**状態の種類:**
- ✅ **接続済み:** トークンが設定され、テスト成功
- ⚙️ **設定中:** トークンが設定されているがテスト未実施
- ❌ **未設定:** トークンが設定されていない
- ⚠️ **エラー:** 接続テストに失敗

**表示情報:**
- 現在の状態
- 最終確認日時（接続テスト実施日時）
- エラーメッセージ（エラー時）

### 5. 削除機能

- 設定済みのトークンを削除
- 確認ダイアログを表示
- 削除後は「未設定」状態に戻る

### 6. トークン取得ガイド

各サービスごとに:
- ステップバイステップのガイド
- 公式ドキュメントへのリンク
- スクリーンショット（オプション）
- 必要な権限の説明

## API連携

### 既存のAPI（利用）

**GET /api/context/sources**
- 現在の設定状態を取得
- フロントエンドで保存したトークンと統合して表示

### 新規API（バックエンド実装が必要）

#### 1. 接続テストAPI

```
POST /api/context/test-connection
```

**機能:**
- 提供されたトークンで実際にサービスに接続
- 権限を確認
- 結果を返す

**実装例（バックエンド）:**
```python
@router.post("/api/context/test-connection")
async def test_connection(request: TestConnectionRequest):
    """
    各サービスへの接続をテスト
    """
    service = request.service

    try:
        if service == "notion":
            # Notionに接続テスト
            token = request.credentials.get("notion_token")
            # 実際の接続テスト処理
            result = await test_notion_connection(token)

        elif service == "slack":
            # Slackに接続テスト
            bot_token = request.credentials.get("slack_bot_token")
            team_id = request.credentials.get("slack_team_id")
            result = await test_slack_connection(bot_token, team_id)

        # ... 他のサービス

        return {
            "success": True,
            "service": service,
            "message": "接続に成功しました",
            "details": result
        }

    except Exception as e:
        return {
            "success": False,
            "service": service,
            "message": "接続に失敗しました",
            "error": {
                "code": "CONNECTION_FAILED",
                "message": str(e),
                "suggestions": [
                    "トークンが正しいか確認してください",
                    "必要な権限が付与されているか確認してください"
                ]
            }
        }
```

#### 2. 設定保存API（オプション）

バックエンドでトークンを管理する場合:

```
POST /api/context/save-credentials
GET /api/context/get-credentials
DELETE /api/context/delete-credentials
```

**注意:** セキュリティのため、バックエンドで保存する場合は暗号化必須。

## データ管理

### ローカルストレージ構造

```typescript
// localStorage key: 'mcp_credentials'
interface MCPCredentials {
  dedalus: {
    api_key: string;
    enabled: boolean;
    last_tested?: string;
    status?: 'connected' | 'error' | 'untested';
  };
  notion: {
    token: string;
    enabled: boolean;
    last_tested?: string;
    status?: 'connected' | 'error' | 'untested';
  };
  slack: {
    bot_token: string;
    team_id: string;
    enabled: boolean;
    last_tested?: string;
    status?: 'connected' | 'error' | 'untested';
    workspace_name?: string;
  };
  atlassian: {
    email: string;
    api_token: string;
    domain: string;
    enabled: boolean;
    last_tested?: string;
    status?: 'connected' | 'error' | 'untested';
  };
}
```

### セキュリティ考慮事項

1. **トークンの暗号化:**
   ```typescript
   // 簡易的なBase64エンコード（最低限）
   function encodeToken(token: string): string {
     return btoa(token);
   }

   function decodeToken(encoded: string): string {
     return atob(encoded);
   }

   // より強固な暗号化（推奨）
   // Web Crypto APIを使用
   ```

2. **HTTPSのみで使用:**
   - 本番環境ではHTTPSを強制

3. **トークンの表示警告:**
   - トークンを表示する際に警告を表示

4. **自動ログアウト:**
   - 一定時間操作がない場合、トークンをマスク

## コンポーネント構成

```
app/
└── settings/
    ├── page.tsx                          # 設定画面メイン
    └── components/
        ├── MCPIntegrationsPanel.tsx      # MCP連携パネル
        ├── DedalusSettings.tsx            # Dedalus設定カード
        ├── NotionSettings.tsx             # Notion設定カード
        ├── SlackSettings.tsx              # Slack設定カード
        ├── AtlassianSettings.tsx          # Atlassian設定カード
        ├── ServiceCard.tsx                # 共通サービスカード
        ├── TokenInput.tsx                 # トークン入力（マスク機能付き）
        ├── ConnectionTestButton.tsx       # 接続テストボタン
        ├── ConnectionTestModal.tsx        # 接続テスト結果モーダル
        ├── SetupGuideModal.tsx            # セットアップガイドモーダル
        ├── StatusBadge.tsx                # ステータスバッジ
        └── ConfirmDialog.tsx              # 確認ダイアログ

hooks/
└── useMCPCredentials.ts                   # トークン管理フック
└── useConnectionTest.ts                   # 接続テストフック

utils/
└── credentialsStorage.ts                  # ストレージ管理
└── credentialsValidator.ts                # バリデーション
└── credentialsEncryption.ts               # 暗号化
```

## カスタムフック

### useMCPCredentials

```typescript
interface MCPCredentialsHook {
  credentials: MCPCredentials;
  loading: boolean;
  saveCredentials: (service: string, creds: any) => Promise<void>;
  deleteCredentials: (service: string) => Promise<void>;
  toggleService: (service: string, enabled: boolean) => void;
  refreshStatus: () => Promise<void>;
}

function useMCPCredentials(): MCPCredentialsHook {
  const [credentials, setCredentials] = useState<MCPCredentials>({});
  const [loading, setLoading] = useState(false);

  // ローカルストレージから読み込み
  useEffect(() => {
    const stored = localStorage.getItem('mcp_credentials');
    if (stored) {
      setCredentials(JSON.parse(stored));
    }
  }, []);

  const saveCredentials = async (service: string, creds: any) => {
    const updated = { ...credentials, [service]: creds };
    localStorage.setItem('mcp_credentials', JSON.stringify(updated));
    setCredentials(updated);
  };

  const deleteCredentials = async (service: string) => {
    const updated = { ...credentials };
    delete updated[service];
    localStorage.setItem('mcp_credentials', JSON.stringify(updated));
    setCredentials(updated);
  };

  const toggleService = (service: string, enabled: boolean) => {
    const updated = {
      ...credentials,
      [service]: { ...credentials[service], enabled }
    };
    localStorage.setItem('mcp_credentials', JSON.stringify(updated));
    setCredentials(updated);
  };

  return { credentials, loading, saveCredentials, deleteCredentials, toggleService, refreshStatus };
}
```

### useConnectionTest

```typescript
interface ConnectionTestHook {
  testing: boolean;
  result: TestConnectionResponse | null;
  testConnection: (service: string, credentials: any) => Promise<void>;
  clearResult: () => void;
}

function useConnectionTest(): ConnectionTestHook {
  const [testing, setTesting] = useState(false);
  const [result, setResult] = useState<TestConnectionResponse | null>(null);

  const testConnection = async (service: string, credentials: any) => {
    setTesting(true);
    try {
      const response = await fetch('/api/context/test-connection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service, credentials }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        service,
        message: '接続テストに失敗しました',
        error: {
          code: 'NETWORK_ERROR',
          message: error.message,
          suggestions: ['ネットワーク接続を確認してください']
        }
      });
    } finally {
      setTesting(false);
    }
  };

  const clearResult = () => setResult(null);

  return { testing, result, testConnection, clearResult };
}
```

## バリデーション

### credentialsValidator.ts

```typescript
interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export function validateDedalusKey(key: string): ValidationResult {
  const errors: string[] = [];

  if (!key || key.trim() === '') {
    errors.push('APIキーは必須です');
  }

  if (key.length < 10) {
    errors.push('APIキーが短すぎます');
  }

  return { valid: errors.length === 0, errors };
}

export function validateNotionToken(token: string): ValidationResult {
  const errors: string[] = [];

  if (!token || token.trim() === '') {
    errors.push('トークンは必須です');
  }

  if (!token.startsWith('secret_')) {
    errors.push('Notionトークンは "secret_" で始まる必要があります');
  }

  return { valid: errors.length === 0, errors };
}

export function validateSlackToken(token: string): ValidationResult {
  const errors: string[] = [];

  if (!token || token.trim() === '') {
    errors.push('Bot Tokenは必須です');
  }

  if (!token.startsWith('xoxb-')) {
    errors.push('Slack Bot Tokenは "xoxb-" で始まる必要があります');
  }

  return { valid: errors.length === 0, errors };
}

export function validateSlackTeamId(teamId: string): ValidationResult {
  const errors: string[] = [];

  if (!teamId || teamId.trim() === '') {
    errors.push('Team IDは必須です');
  }

  if (!teamId.startsWith('T')) {
    errors.push('Slack Team IDは "T" で始まる必要があります');
  }

  return { valid: errors.length === 0, errors };
}

export function validateAtlassianEmail(email: string): ValidationResult {
  const errors: string[] = [];
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!email || email.trim() === '') {
    errors.push('メールアドレスは必須です');
  }

  if (!emailRegex.test(email)) {
    errors.push('有効なメールアドレスを入力してください');
  }

  return { valid: errors.length === 0, errors };
}

export function validateAtlassianToken(token: string): ValidationResult {
  const errors: string[] = [];

  if (!token || token.trim() === '') {
    errors.push('API Tokenは必須です');
  }

  if (!token.startsWith('ATATT')) {
    errors.push('Atlassian API Tokenは "ATATT" で始まる必要があります');
  }

  return { valid: errors.length === 0, errors };
}

export function validateAtlassianDomain(domain: string): ValidationResult {
  const errors: string[] = [];

  if (!domain || domain.trim() === '') {
    errors.push('ドメインは必須です');
  }

  if (!domain.endsWith('.atlassian.net')) {
    errors.push('ドメインは ".atlassian.net" で終わる必要があります');
  }

  return { valid: errors.length === 0, errors };
}
```

## UI/UXガイドライン

### カラーパレット

```css
/* サービスカラー */
--dedalus-color: #6366F1;     /* Indigo */
--notion-color: #000000;
--slack-color: #4A154B;
--atlassian-color: #0052CC;

/* ステータスカラー */
--status-connected: #10B981;   /* Green */
--status-error: #EF4444;       /* Red */
--status-untested: #6B7280;    /* Gray */
--status-testing: #F59E0B;     /* Amber */
```

### アイコン

- **Dedalus:** ⚙️ または 🔷
- **Notion:** 📓
- **Slack:** 💬
- **Atlassian:** 🔷
- **接続済み:** ✅
- **エラー:** ❌
- **警告:** ⚠️
- **情報:** ℹ️

### インタラクション

1. **トークン入力:**
   - フォーカス時に枠線の色を変更
   - エラー時は赤色の枠線とメッセージ

2. **接続テストボタン:**
   - クリック時にローディングスピナー表示
   - 成功時に緑色のチェックマークアニメーション
   - 失敗時に赤色のXマークアニメーション

3. **保存ボタン:**
   - 変更がない場合は無効化（グレーアウト）
   - 保存成功時にトースト通知

4. **削除ボタン:**
   - 確認ダイアログを表示
   - 削除後にトースト通知

### レスポンシブデザイン

- **モバイル（< 768px）:**
  - 1カラムレイアウト
  - カードを縦に積む
  - ボタンを全幅に

- **タブレット（768px - 1024px）:**
  - 2カラムレイアウト
  - カードを横に2つ並べる

- **デスクトップ（> 1024px）:**
  - サイドバー + メインコンテンツ
  - カードを横に2-3つ並べる

## エラーハンドリング

### ユーザーに表示するエラーメッセージ

1. **バリデーションエラー:**
   ```
   入力内容に誤りがあります
   - Notionトークンは "secret_" で始まる必要があります
   ```

2. **接続エラー:**
   ```
   Slackとの接続に失敗しました
   - Bot Tokenが無効です
   - 必要な権限が付与されていません

   [再試行]  [ヘルプを見る]
   ```

3. **保存エラー:**
   ```
   設定の保存に失敗しました
   もう一度お試しください
   ```

## アクセシビリティ

- キーボードナビゲーション完全対応
- スクリーンリーダー対応（aria-label追加）
- カラーコントラスト比 4.5:1 以上
- エラーメッセージは視覚と音声の両方で通知

## パフォーマンス

- 接続テストのタイムアウト: 10秒
- デバウンス処理（入力中の自動保存防止）
- 大きなトークンリストも対応（仮想スクロール不要）

## テスト要件

### ユニットテスト
- バリデーション関数のテスト
- 暗号化/復号化のテスト
- カスタムフックのテスト

### インテグレーションテスト
- 接続テストAPIのテスト
- ローカルストレージの読み書きテスト

### E2Eテスト
- トークン設定フローのテスト
- 接続テストのテスト
- 削除フローのテスト

## 実装の優先順位

### Phase 1: 基本機能
1. ✅ 設定画面のレイアウト
2. ✅ トークン入力フォーム
3. ✅ ローカルストレージへの保存
4. ✅ バリデーション

### Phase 2: 接続テスト
1. ✅ 接続テストAPI実装（バックエンド）
2. ✅ 接続テストボタンとモーダル
3. ✅ ステータス表示

### Phase 3: UX改善
1. ✅ トークン取得ガイドモーダル
2. ✅ トースト通知
3. ✅ アニメーション
4. ✅ レスポンシブデザイン

### Phase 4: 高度な機能
1. ⏳ バックエンドでのトークン管理（オプション）
2. ⏳ トークンの暗号化強化
3. ⏳ 定期的な接続確認
4. ⏳ 使用状況の統計表示

## セキュリティチェックリスト

- [ ] トークンをlocalStorageに保存する際は暗号化
- [ ] HTTPS通信のみ許可
- [ ] トークン表示時に警告を表示
- [ ] XSS対策（入力値のサニタイゼーション）
- [ ] CSRF対策（APIトークン使用時）
- [ ] コンソールログにトークンを出力しない
- [ ] エラーメッセージにトークンを含めない

## 参考リンク

- [Notion API Documentation](https://developers.notion.com/)
- [Slack API Documentation](https://api.slack.com/)
- [Atlassian API Documentation](https://developer.atlassian.com/)
- [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
