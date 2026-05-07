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

MAIN_PAGE = "357d229a-1c28-80b8-a82b-c382a1425005"

def get_all_children(page_id):
    url  = f"https://api.notion.com/v1/blocks/{page_id}/children"
    res  = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(f"  ❌ 오류: {res.json().get('message','')}")
        return []
    return res.json().get("results", [])

def search_databases():
    url  = "https://api.notion.com/v1/search"
    body = {
        "filter": {"value": "database", "property": "object"},
        "page_size": 100
    }
    res  = requests.post(url, headers=HEADERS, json=body)
    if res.status_code != 200:
        print(f"  ❌ 오류: {res.json().get('message','')}")
        return []
    return res.json().get("results", [])

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 실제 DB ID 조회 시작!")
    print("=" * 60)

    print("\n📋 통합에 연결된 모든 DB 목록:")
    dbs = search_databases()
    for db in dbs:
        title = db.get("title", [{}])
        name  = title[0].get("plain_text", "제목없음") if title else "제목없음"
        db_id = db.get("id", "")
        print(f"  📁 {name}")
        print(f"     ID: {db_id}")

    print("\n" + "=" * 60)
    print(f"🎉 총 {len(dbs)}개 DB 발견!")
    print("=" * 60)