# Backend

FastAPI backend application.

## セットアップ

1. 環境変数ファイルをコピー：
```bash
cp .env.example .env
```

2. 依存関係をインストール：
```bash
pip3 install -r requirements.txt
```

## 起動

```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

または、ルートディレクトリから：
```bash
make dev-backend
```

## 設定

環境変数は`config.py`で管理されています。`.env`ファイルで設定をカスタマイズできます。
