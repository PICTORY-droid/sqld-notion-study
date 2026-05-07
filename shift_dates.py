import requests
import os
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

PLAN_DB = "357d229a-1c28-81d0-b594-c3ff7c081a26"

def get_all_pages():
    pages = []
    url   = f"https://api.notion.com/v1/databases/{PLAN_DB}/query"
    body  = {
        "sorts": [{"property": "학습날짜", "direction": "ascending"}],
        "page_size": 100
    }
    while True:
        res  = requests.post(url, headers=HEADERS, json=body)
        data = res.json()
        pages.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        body["start_cursor"] = data["next_cursor"]
    return pages

def shift_date(page_id, current_date_str):
    current = date.fromisoformat(current_date_str)
    new_date = (current + timedelta(days=1)).isoformat()
    url  = f"https://api.notion.com/v1/pages/{page_id}"
    body = {
        "properties": {
            "학습날짜": {"date": {"start": new_date}}
        }
    }
    res = requests.patch(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"  ✅ {current_date_str} → {new_date}")
    else:
        print(f"  ❌ 오류: {res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 50)
    print("📅 날짜 하루 뒤로 이동 시작!")
    print("   2026-05-06 → 2026-05-07 부터 시작")
    print("=" * 50)

    pages = get_all_pages()
    print(f"\n총 {len(pages)}개 페이지 로드 완료\n")

    for page in pages:
        date_prop = page["properties"].get("학습날짜", {}).get("date")
        if date_prop and date_prop.get("start"):
            shift_date(page["id"], date_prop["start"])
        else:
            print(f"  ⚠️ 날짜 없는 페이지 건너뜀: {page['id']}")

    print("\n" + "=" * 50)
    print(f"🎉 총 {len(pages)}개 날짜 이동 완료!")
    print("   시작일: 2026-05-07")
    print("   종료일: 2026-08-22")
    print("=" * 50)