import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
THEORY_DB_ID = "357d229a-1c28-81e9-a858-ca17697f7429"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_theory(name, date, subject, understanding):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": THEORY_DB_ID},
        "properties": {
            "단원명":   {"title": [{"text": {"content": name}}]},
            "학습일":   {"date": {"start": date}},
            "과목":     {"select": {"name": subject}},
            "이해도":   {"select": {"name": understanding}},
            "복습필요": {"checkbox": False},
            "완료":     {"checkbox": False},
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
  python add_theory.py "단원명" "날짜" "과목" "이해도"

과목 옵션 (그대로 복사하세요):
  "1과목 - 데이터 모델링"
  "2과목 - SQL 기본 및 활용"

이해도 옵션 (그대로 복사하세요):
  "⭐ 잘 모름"
  "⭐⭐ 조금 앎"
  "⭐⭐⭐ 보통"
  "⭐⭐⭐⭐ 잘 앎"
  "⭐⭐⭐⭐⭐ 완벽"

예시:
  python add_theory.py "엔터티와 속성" "2026-05-06" "1과목 - 데이터 모델링" "⭐⭐⭐ 보통"
""")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print_usage()
    else:
        add_theory(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])