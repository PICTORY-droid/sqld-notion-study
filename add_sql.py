import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
SQL_DB_ID = "357d229a-1c28-8126-ba08-e099b68a2cf3"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_sql(name, date, category, difficulty):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": SQL_DB_ID},
        "properties": {
            "문법명":   {"title": [{"text": {"content": name}}]},
            "실습일":   {"date": {"start": date}},
            "분류":     {"select": {"name": category}},
            "난이도":   {"select": {"name": difficulty}},
            "오류발생": {"checkbox": False},
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
  python add_sql.py "문법명" "날짜" "분류" "난이도"

분류 옵션 (그대로 복사하세요):
  "SELECT (조회)"
  "WHERE (조건)"
  "JOIN (연결)"
  "GROUP BY (그룹)"
  "서브쿼리"
  "윈도우함수"
  "DDL (테이블 생성)"
  "DML (데이터 조작)"

난이도 옵션 (그대로 복사하세요):
  "쉬움"
  "보통"
  "어려움"

예시:
  python add_sql.py "GROUP BY 실습" "2026-05-06" "GROUP BY (그룹)" "보통"
""")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print_usage()
    else:
        add_sql(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])