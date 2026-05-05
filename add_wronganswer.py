import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
WRONGANSWER_DB_ID = "357d229a-1c28-8186-ba13-f81e4159f1e4"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def add_wronganswer(item, date, reason, memo):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": WRONGANSWER_DB_ID},
        "properties": {
            "오답항목":   {"title": [{"text": {"content": item}}]},
            "틀린날짜":   {"date": {"start": date}},
            "틀린이유":   {"select": {"name": reason}},
            "오답메모":   {"rich_text": [{"text": {"content": memo}}]},
            "재풀이완료": {"checkbox": False},
        },
        "children": [
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "📌 틀린 이유"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": reason}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "📝 오답 메모"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": memo}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "🔁 재풀이 메모"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": "재풀이 후 여기에 추가로 메모하세요!"}}]
                            }
                        }
                    ]
                }
            },
        ]
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"✅ 추가 완료! → {item}")
    else:
        print(f"❌ 오류: {res.json().get('message','')}")

def print_usage():
    print("""
사용법:
  python add_wronganswer.py "오답항목" "틀린날짜" "틀린이유" "오답메모"

틀린이유 옵션 (그대로 복사하세요):
  "개념을 몰랐음"
  "문제를 잘못 읽음"
  "헷갈리는 개념"
  "계산 실수"
  "시간 부족"

예시:
  python add_wronganswer.py "NULL 비교 문제" "2026-05-06" "개념을 몰랐음" "NULL은 IS NULL로 비교해야 함. = 으로 비교하면 안됨"
""")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print_usage()
    else:
        add_wronganswer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])