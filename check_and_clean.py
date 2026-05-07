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

# 실제 사용 중인 DB (보존)
REAL_DBS = {
    "📅 학습 계획 DB":    "357d229a-1c28-81d0-b594-c3ff7c081a26",
    "📖 이론 학습 DB":    "357d229a-1c28-81e9-a858-ca17697f7429",
    "💻 SQL 실습 DB":     "357d229a-1c28-8126-ba08-e099b68a2cf3",
    "🃏 플래시카드 DB":   "357d229a-1c28-8184-b66d-cbff67aa585a",
    "📖 SQL 레퍼런스 DB": "357d229a-1c28-81e6-848e-c343119beb87",
    "❓ 문제풀이 DB":     "357d229a-1c28-816d-b080-c10b7b4cc44e",
    "📝 오답 노트 DB":    "357d229a-1c28-8186-ba13-f81e4159f1e4",
    "❌ 오답 패턴 DB":    "357d229a-1c28-81b0-bcf0-c2a2f8cd7f5b",
    "🔁 복습 스케줄 DB":  "357d229a-1c28-8168-9d60-cd4d3379cc93",
}

# 삭제할 중복 DB
DUPLICATE_DBS = {
    "📅 학습 계획 DB (중복1)": "357d229a-1c28-8131-88d4-cc3bd4f6376d",
    "📅 학습 계획 DB (중복2)": "357d229a-1c28-81a4-9035-e3ec834a51db",
    "📖 이론 학습 DB (중복1)": "357d229a-1c28-81a8-ac6c-dc8debd522ba",
    "📖 이론 학습 DB (중복2)": "357d229a-1c28-81bc-bdca-f2f32d27beee",
    "💻 SQL 실습 DB (중복1)":  "357d229a-1c28-8163-935b-d8f05f2e49ac",
    "💻 SQL 실습 DB (중복2)":  "357d229a-1c28-8189-8082-d9fca6c9aedd",
    "🔁 복습 스케줄 DB (중복1)":"357d229a-1c28-81e1-b8db-cde7fa6e129b",
    "🔁 복습 스케줄 DB (중복2)":"357d229a-1c28-81fa-ad86-df13a0f9fd34",
    "❓ 문제풀이 DB (중복1)":  "357d229a-1c28-8197-b07d-f7c229e21d7d",
    "❓ 문제풀이 DB (중복2)":  "357d229a-1c28-817e-9a36-e088a1a3b731",
    "📝 오답 노트 DB (중복1)": "357d229a-1c28-81ef-afff-fd2d641245bf",
    "📝 오답 노트 DB (중복2)": "357d229a-1c28-811d-866c-eb970dd83d75",
    "❌ 오답 패턴 DB (중복1)": "357d229a-1c28-81b0-9eaa-da256e7793ff",
    "❌ 오답 패턴 DB (중복2)": "357d229a-1c28-8166-9c91-d55d90ab1b2f",
    "📖 SQL 레퍼런스 DB (중복1)":"357d229a-1c28-8163-b50a-d8039e5ab44e",
    "📖 SQL 레퍼런스 DB (중복2)":"357d229a-1c28-8135-af7a-ff4f5d3a0d06",
    "🃏 플래시카드 DB (중복1)": "357d229a-1c28-8114-b307-e625a491df58",
    "🃏 플래시카드 DB (중복2)": "357d229a-1c28-810d-b6f8-cd2ed977ebd1",
}

def check_relations(name, db_id):
    url = f"https://api.notion.com/v1/databases/{db_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(f"  ❌ {name} 조회 실패")
        return
    props = res.json().get("properties", {})
    relations = [(k, v.get("relation", {}).get("database_id", ""))
                 for k, v in props.items() if v.get("type") == "relation"]
    if relations:
        print(f"\n  🔗 {name} 릴레이션:")
        for rel_name, rel_db in relations:
            check = requests.get(f"https://api.notion.com/v1/databases/{rel_db}", headers=HEADERS)
            if check.status_code == 200:
                linked = check.json().get("title", [{}])[0].get("plain_text", "이름없음")
                status = "✅ 정상" if rel_db in REAL_DBS.values() else "⚠️ 중복DB 연결됨!"
                print(f"    {status} '{rel_name}' → '{linked}'")
            else:
                print(f"    ❌ '{rel_name}' → 연결 오류!")
    else:
        print(f"  ℹ️  {name}: 릴레이션 없음")

def archive_page(name, page_id):
    url  = f"https://api.notion.com/v1/pages/{page_id}"
    body = {"archived": True}
    res  = requests.patch(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"  🗑️  {name} — 삭제 완료")
    else:
        print(f"  ❌ {name} — 삭제 실패: {res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 60)
    print("① 실제 사용 중인 DB 릴레이션 점검")
    print("=" * 60)
    for name, db_id in REAL_DBS.items():
        check_relations(name, db_id)

    print("\n" + "=" * 60)
    print("② 중복 DB 삭제 (노션 휴지통으로 이동)")
    print("=" * 60)
    for name, db_id in DUPLICATE_DBS.items():
        archive_page(name, db_id)

    print("\n" + "=" * 60)
    print("🎉 점검 및 정리 완료!")
    print("=" * 60)