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

# 중복된 DB 전체 목록 (이름별로 그룹화)
DBS = {
    "📅 학습 계획 DB": [
        "357d229a-1c28-81d0-b594-c3ff7c081a26",
        "357d229a-1c28-8131-88d4-cc3bd4f6376d",
        "357d229a-1c28-81a4-9035-e3ec834a51db",
    ],
    "📖 이론 학습 DB": [
        "357d229a-1c28-81a8-ac6c-dc8debd522ba",
        "357d229a-1c28-81bc-bdca-f2f32d27beee",
        "357d229a-1c28-81e9-a858-ca17697f7429",
    ],
    "💻 SQL 실습 DB": [
        "357d229a-1c28-8163-935b-d8f05f2e49ac",
        "357d229a-1c28-8189-8082-d9fca6c9aedd",
        "357d229a-1c28-8126-ba08-e099b68a2cf3",
    ],
    "🔁 복습 스케줄 DB": [
        "357d229a-1c28-81e1-b8db-cde7fa6e129b",
        "357d229a-1c28-81fa-ad86-df13a0f9fd34",
        "357d229a-1c28-8168-9d60-cd4d3379cc93",
    ],
    "❓ 문제풀이 DB": [
        "357d229a-1c28-8197-b07d-f7c229e21d7d",
        "357d229a-1c28-817e-9a36-e088a1a3b731",
        "357d229a-1c28-816d-b080-c10b7b4cc44e",
    ],
    "📝 오답 노트 DB": [
        "357d229a-1c28-81ef-afff-fd2d641245bf",
        "357d229a-1c28-811d-866c-eb970dd83d75",
        "357d229a-1c28-8186-ba13-f81e4159f1e4",
    ],
    "❌ 오답 패턴 DB": [
        "357d229a-1c28-81b0-9eaa-da256e7793ff",
        "357d229a-1c28-8166-9c91-d55d90ab1b2f",
        "357d229a-1c28-81b0-bcf0-c2a2f8cd7f5b",
    ],
    "📖 SQL 레퍼런스 DB": [
        "357d229a-1c28-8163-b50a-d8039e5ab44e",
        "357d229a-1c28-8135-af7a-ff4f5d3a0d06",
        "357d229a-1c28-81e6-848e-c343119beb87",
    ],
    "🃏 플래시카드 DB": [
        "357d229a-1c28-8114-b307-e625a491df58",
        "357d229a-1c28-810d-b6f8-cd2ed977ebd1",
        "357d229a-1c28-8184-b66d-cbff67aa585a",
    ],
}

def get_db_row_count(db_id):
    url  = f"https://api.notion.com/v1/databases/{db_id}/query"
    res  = requests.post(url, headers=HEADERS, json={"page_size": 1})
    if res.status_code != 200:
        return -1
    data = res.json()
    # 전체 개수는 직접 세야 함
    count = 0
    body  = {"page_size": 100}
    while True:
        r = requests.post(url, headers=HEADERS, json=body)
        d = r.json()
        count += len(d.get("results", []))
        if not d.get("has_more"):
            break
        body["start_cursor"] = d["next_cursor"]
    return count

def get_parent_info(db_id):
    url = f"https://api.notion.com/v1/databases/{db_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return "조회실패"
    parent = res.json().get("parent", {})
    ptype  = parent.get("type", "")
    if ptype == "page_id":
        return f"페이지 하위 ({parent.get('page_id','')})"
    elif ptype == "workspace":
        return "워크스페이스 최상위"
    return ptype

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 실제 사용 중인 DB 찾기 (데이터 수 기준)")
    print("=" * 60)

    real_dbs = {}

    for name, ids in DBS.items():
        print(f"\n📋 {name}")
        best_id    = None
        best_count = -1
        for db_id in ids:
            count  = get_db_row_count(db_id)
            parent = get_parent_info(db_id)
            marker = ""
            if count > best_count:
                best_count = count
                best_id    = db_id
            print(f"  {'★' if count == max([get_db_row_count(i) for i in ids]) else ' '} ID: {db_id}")
            print(f"    데이터: {count}개 | 위치: {parent}")
        real_dbs[name] = (best_id, best_count)

    print("\n" + "=" * 60)
    print("✅ 데이터가 가장 많은 DB (실제 사용 중인 것)")
    print("=" * 60)
    for name, (db_id, count) in real_dbs.items():
        print(f"  {name}: {db_id} ({count}개)")