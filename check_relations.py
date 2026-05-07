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

# 알려진 DB ID 전체
DBS = {
    "📅 학습 계획":     "357d229a-1c28-81d0-b594-c3ff7c081a26",
    "📖 이론 학습":     "357d229a-1c28-8198-8d37-dece7c78f5b4",
    "💻 SQL 실습":      "357d229a-1c28-8172-898b-d4d3adeac8f2",
    "🔁 복습 스케줄":   "357d229a-1c28-81b7-a06b-c5a7c7c0c1f3",
    "❓ 문제풀이":      "357d229a-1c28-8135-baae-e93f82b4a6c1",
    "📝 오답 노트":     "357d229a-1c28-8116-8cf6-c4e3b74e9f2a",
}

def get_db_info(db_id, name):
    url = f"https://api.notion.com/v1/databases/{db_id}"
    res = requests.get(url, headers=HEADERS)

    print(f"\n{'='*50}")
    print(f"📋 {name}")
    print(f"{'='*50}")

    if res.status_code != 200:
        print(f"  ❌ DB 조회 실패 (ID가 틀렸거나 접근 불가): {res.json().get('message','')}")
        return

    data  = res.json()
    props = data.get("properties", {})

    relations = [(k, v.get("relation", {}).get("database_id", "")) 
                 for k, v in props.items() if v.get("type") == "relation"]

    if relations:
        print(f"  🔗 릴레이션 ({len(relations)}개):")
        for rel_name, rel_db in relations:
            check = requests.get(f"https://api.notion.com/v1/databases/{rel_db}", headers=HEADERS)
            if check.status_code == 200:
                linked = check.json().get("title", [{}])[0].get("plain_text", "이름없음")
                print(f"    ✅ '{rel_name}' → '{linked}' (정상)")
            else:
                print(f"    ❌ '{rel_name}' → 연결 오류! (DB ID: {rel_db})")
    else:
        print(f"  ℹ️  릴레이션 없음")

    print(f"  📊 속성 목록: {', '.join(props.keys())}")

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 전체 DB 릴레이션 점검 시작!")
    print("=" * 50)

    for name, db_id in DBS.items():
        get_db_info(db_id, name)

    print("\n" + "=" * 50)
    print("🎉 전체 점검 완료!")
    print("=" * 50)