from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class SurveyRequest(BaseModel):
    mode: str  # "trend", "account", "keyword", "idea"
    input: str

@app.get("/")
def root():
    return {"status": "ok", "message": "X Survey App API"}

@app.post("/survey")
def survey(req: SurveyRequest):
    prompt = build_prompt(req.mode, req.input)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = ""
    for block in response.content:
        if hasattr(block, "text"):
            result += block.text
    
    return {"result": result}

def build_prompt(mode: str, input: str) -> str:
    prompts = {
        "trend": f"""
以下のジャンル・キーワードについて、X（Twitter）や各種メディアで今話題になっているトピックをweb検索で調査してください。

ジャンル・キーワード：{input}

以下の形式で出力してください：
1. 今熱いトピック（3〜5個）
2. 各トピックの要約（2〜3行）
3. YouTube動画ネタとしての可能性コメント
""",
        "account": f"""
X（Twitter）の以下のアカウントについてweb検索で調査し、分析してください。

アカウント：{input}

以下の形式で出力してください：
1. アカウントの概要・特徴
2. よく扱うテーマ・トピック
3. 人気コンテンツの傾向
4. YouTube動画ネタとして参考になる点
""",
        "keyword": f"""
以下のキーワードについて、X（Twitter）や各種メディアでの話題をweb検索で調査してください。

キーワード：{input}

以下の形式で出力してください：
1. このキーワードを巡る主な議論・話題
2. 異なる切り口・角度（3〜5個）
3. YouTube動画ネタとしての切り口候補
""",
        "idea": f"""
以下の調査結果をもとに、YouTube動画のネタ候補を生成してください。

調査結果：{input}

以下の形式で出力してください：
1. 動画タイトル案（3〜5個）
2. 各タイトルの概要・構成案
3. 想定視聴者
4. video_prompt案（Runway用）
"""
    }
    return prompts.get(mode, f"{input}についてweb検索で調査して日本語で報告してください。")