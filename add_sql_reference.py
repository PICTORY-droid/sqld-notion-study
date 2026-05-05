import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
SQL_REFERENCE_DB_ID = "357d229a-1c28-81e6-848e-c343119beb87"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_sql_reference(name, code, description, category):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": SQL_REFERENCE_DB_ID},
        "properties": {
            "문법이름": {"title": [{"text": {"content": name}}]},
            "코드":     {"rich_text": [{"text": {"content": code}}]},
            "설명":     {"rich_text": [{"text": {"content": description}}]},
            "유형":     {"select": {"name": category}},
            "자주출제": {"checkbox": False},
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
  python add_sql_reference.py "문법이름" "코드" "설명" "유형"

유형 옵션 (그대로 복사하세요):
  "SELECT / FROM"
  "WHERE 조건"
  "JOIN"
  "집계함수"
  "서브쿼리"
  "DDL"
  "DML"
  "DCL / TCL"

예시:
  python add_sql_reference.py "GROUP BY" "SELECT 컬럼, COUNT(*) FROM 테이블 GROUP BY 컬럼;" "특정 컬럼을 기준으로 데이터를 그룹화할 때 사용" "집계함수"
""")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print_usage()
    else:
        add_sql_reference(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])