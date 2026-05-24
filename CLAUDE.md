# CLAUDE.md — x-survey-app（バックエンド）

## プロジェクト概要
YouTubeネタ発掘のためのサーベイツール（バックエンドAPI）

## 技術スタック
- Python 3.13
- FastAPI
- Anthropic Claude API（web_search tool使用）
- uvicorn

## ディレクトリ構成
x-survey-app/
├── main.py         # メインAPI
├── .env            # APIキー（ローカルのみ）
├── requirements.txt
├── render.yaml
└── venv/

## 主要エンドポイント
- GET  /         → ヘルスチェック
- POST /survey   → サーベイ実行（mode, inputを受け取る）

## サーベイモード
- trend    : トレンド分析
- account  : アカウント分析
- keyword  : キーワード調査
- idea     : ネタ生成

## ローカル起動
source venv/bin/activate
uvicorn main:app --reload

## デプロイ
- GitHub: https://github.com/yamanoazalea-ship-it/x-survey-app
- Render: https://x-survey-app.onrender.com
- GitHubにpushすると自動デプロイ

## 環境変数
- ANTHROPIC_API_KEY: Anthropic APIキー（Renderの環境変数に設定済み）

## 注意事項
- .envはGitにコミットしない
- venvはGitにコミットしない
- Claude APIのweb_searchツールを使ってサーベイを実行している
