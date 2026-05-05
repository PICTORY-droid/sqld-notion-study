import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
WRONG_PATTERN_DB_ID = "357d229a-1c28-81b0-bcf0-c2a2f8cd7f5b"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_wrong_pattern(number, content, explanation, reason, unit):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": WRONG_PATTERN_DB_ID},
        "properties": {
            "문제번호": {"title": [{"text": {"content": number}}]},
            "틀린내용": {"rich_text": [{"text": {"content": content}}]},
            "정답해설": {"rich_text": [{"text": {"content": explanation}}]},
            "틀린이유": {"select": {"name": reason}},
            "단원":     {"select": {"name": unit}},
            "반복실수": {"checkbox": False},
        }
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"✅ 추가 완료! → {number} 문제")
    else:
        print(f"❌ 오류: {res.json().get('message','')}")

def print_usage():
    print("""
사용법:
  python add_wrong_pattern.py "문제번호" "틀린내용" "정답해설" "틀린이유" "단원"

틀린이유 옵션 (그대로 복사하세요):
  "개념 이해 부족"
  "문제 오독"
  "계산 실수"
  "헷갈리는 용어"

단원 옵션 (그대로 복사하세요):
  "1과목 - 데이터 모델링의 이해"
  "1과목 - 데이터 모델과 SQL"
  "2과목 - SQL 기본"
  "2과목 - SQL 활용"
  "2과목 - 관리 구문"

예시:
  python add_wrong_pattern.py "15번" "엔터티와 인스턴스를 혼동함" "엔터티는 집합, 인스턴스는 엔터티의 하나의 행" "헷갈리는 용어" "1과목 - 데이터 모델링의 이해"
""")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print_usage()
    else:
        add_wrong_pattern(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])