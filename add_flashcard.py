import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
FLASHCARD_DB_ID = "357d229a-1c28-8184-b66d-cbff67aa585a"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_flashcard(keyword, question, answer, unit, difficulty):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": FLASHCARD_DB_ID},
        "properties": {
            "키워드": {"title": [{"text": {"content": keyword}}]},
            "질문":   {"rich_text": [{"text": {"content": question}}]},
            "답":     {"rich_text": [{"text": {"content": answer}}]},
            "단원":   {"select": {"name": unit}},
            "난이도": {"select": {"name": difficulty}},
            "암기완료": {"checkbox": False},
        }
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"✅ 추가 완료! → {keyword}")
    else:
        print(f"❌ 오류: {res.json().get('message','')}")

def print_usage():
    print("""
사용법:
  python add_flashcard.py "키워드" "질문" "답" "단원" "난이도"

단원 옵션:
  1과목 - 데이터 모델링의 이해
  1과목 - 데이터 모델과 SQL
  2과목 - SQL 기본
  2과목 - SQL 활용
  2과목 - 관리 구문

난이도 옵션:
  ⭐ 쉬움
  ⭐⭐ 보통
  ⭐⭐⭐ 어려움

예시:
  python add_flashcard.py "엔터티" "엔터티란?" "독립적으로 존재하는 사람, 사물, 개념의 집합" "1과목 - 데이터 모델링의 이해" "⭐ 쉬움"
""")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print_usage()
    else:
        add_flashcard(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])