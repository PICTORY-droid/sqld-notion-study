import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
QUIZ_DB_ID = "357d229a-1c28-816d-b080-c10b7b4cc44e"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_quiz(name, date, source, subject, result, difficulty):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": QUIZ_DB_ID},
        "properties": {
            "문제명":       {"title": [{"text": {"content": name}}]},
            "풀이날짜":     {"date": {"start": date}},
            "출처":         {"select": {"name": source}},
            "과목":         {"select": {"name": subject}},
            "정답여부":     {"select": {"name": result}},
            "난이도":       {"select": {"name": difficulty}},
            "오답노트작성": {"checkbox": False},
        }
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"✅ 추가 완료! → {name}")
    else:
        print(f"❌ 오류: {res.json().get('message','')}")

def print_usage():
    print("""
사용법:
  python add_quiz.py "문제명" "날짜" "출처" "과목" "정답여부" "난이도"

출처 옵션 (그대로 복사하세요):
  "이기적 교재"
  "기출문제"
  "모의고사"
  "인터넷 문제"

과목 옵션 (그대로 복사하세요):
  "1과목"
  "2과목"

정답여부 옵션 (그대로 복사하세요):
  "✅ 정답"
  "❌ 오답"
  "🤔 찍음"

난이도 옵션 (그대로 복사하세요):
  "쉬움"
  "보통"
  "어려움"

예시:
  python add_quiz.py "엔터티 식별자 문제" "2026-05-06" "이기적 교재" "1과목" "❌ 오답" "보통"
""")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print_usage()
    else:
        add_quiz(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])