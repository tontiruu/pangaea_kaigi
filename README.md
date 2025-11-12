# Pangaea Kaigi

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

| 変数名 | 説明 | デフォルト値 |
|--------|------|--------------|
| `DEBUG` | デバッグモード | `True` |
| `APP_NAME` | アプリケーション名 | `Pangaea Kaigi API` |
| `API_VERSION` | APIバージョン | `0.1.0` |
| `HOST` | サーバーホスト | `0.0.0.0` |
| `PORT` | サーバーポート | `8000` |
| `CORS_ORIGINS` | CORS許可オリジン（カンマ区切り） | `http://localhost:3000,http://127.0.0.1:3000` |
