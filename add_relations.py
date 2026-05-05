import requests
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# DB ID 목록
THEORY_DB      = "357d229a-1c28-81e9-a858-ca17697f7429"
SQL_DB         = "357d229a-1c28-8126-ba08-e099b68a2cf3"
REVIEW_DB      = "357d229a-1c28-8168-9d60-cd4d3379cc93"
QUIZ_DB        = "357d229a-1c28-816d-b080-c10b7b4cc44e"
WRONGANSWER_DB = "357d229a-1c28-8186-ba13-f81e4159f1e4"
PLAN_DB        = "357d229a-1c28-81d0-b594-c3ff7c081a26"

def add_relation(db_id, property_name, target_db_id):
    url  = f"https://api.notion.com/v1/databases/{db_id}"
    body = {
        "properties": {
            property_name: {
                "relation": {
                    "database_id": target_db_id,
                    "single_property": {}
                }
            }
        }
    }
    res = requests.patch(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"  ✅ 연결 완료: {property_name}")
    else:
        print(f"  ❌ 오류: {res.json().get('message','')}")

print("=" * 50)
print("🔗 릴레이션 연결 시작!")
print("=" * 50)

# 이론학습 ↔ 복습스케줄
print("\n📖 이론학습 DB → 복습스케줄 DB 연결")
add_relation(THEORY_DB, "복습스케줄", REVIEW_DB)

# 이론학습 ↔ 학습계획
print("\n📖 이론학습 DB → 학습계획 DB 연결")
add_relation(THEORY_DB, "학습계획", PLAN_DB)

# 문제풀이 ↔ 오답노트
print("\n❓ 문제풀이 DB → 오답노트 DB 연결")
add_relation(QUIZ_DB, "오답노트", WRONGANSWER_DB)

# 문제풀이 ↔ 이론학습
print("\n❓ 문제풀이 DB → 이론학습 DB 연결")
add_relation(QUIZ_DB, "관련이론", THEORY_DB)

# 오답노트 ↔ 이론학습
print("\n📝 오답노트 DB → 이론학습 DB 연결")
add_relation(WRONGANSWER_DB, "관련이론", THEORY_DB)

# SQL실습 ↔ 학습계획
print("\n💻 SQL실습 DB → 학습계획 DB 연결")
add_relation(SQL_DB, "학습계획", PLAN_DB)

print("\n" + "=" * 50)
print("🎉 릴레이션 연결 완료!")
print("=" * 50)