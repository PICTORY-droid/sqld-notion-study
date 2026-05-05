import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PLAN_DB_ID = "357d229a-1c28-81d0-b594-c3ff7c081a26"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_plan(goal, date, study_type, target_min):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": PLAN_DB_ID},
        "properties": {
            "학습목표":    {"title": [{"text": {"content": goal}}]},
            "학습날짜":    {"date": {"start": date}},
            "유형":        {"select": {"name": study_type}},
            "목표시간_분": {"number": int(target_min)},
            "완료":        {"checkbox": False},
        }
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"✅ 추가 완료! → {goal}")
    else:
        print(f"❌ 오류: {res.json().get('message','')}")

def print_usage():
    print("""
사용법:
  python add_plan.py "학습목표" "날짜" "유형" "목표시간(분)"

유형 옵션 (그대로 복사하세요):
  "이론학습"   ← 교재 읽고 개념 공부한 날
  "SQL실습"    ← SQL 문법 직접 써보는 날
  "문제풀이"   ← 기출문제나 연습문제 푸는 날
  "복습"       ← 전에 공부한 내용 다시 보는 날
  "오답정리"   ← 틀린 문제 다시 정리하는 날

예시:
  python add_plan.py "엔터티와 속성 개념 공부" "2026-05-06" "이론학습" 60
""")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print_usage()
    else:
        add_plan(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])