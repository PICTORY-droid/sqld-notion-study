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

# 통일할 이모지 URL
EMOJI = {
    "type": "external",
    "external": {"url": "https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/25aa-fe0f.svg"}
}

def get_blocks(page_id):
    res = requests.get(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=HEADERS)
    return res.json().get("results", [])

def delete_block(block_id):
    requests.delete(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS)

def unify_page(page_id, page_name):
    print(f"\n🔧 {page_name} 통일 중...")
    blocks = get_blocks(page_id)
    for block in blocks:
        block_type = block["type"]
        block_id   = block["id"]

        # 콜아웃 → 기본색(흰색) + 이모지 통일
        if block_type == "callout":
            body = {
                "callout": {
                    "rich_text": block["callout"]["rich_text"],
                    "icon": EMOJI,
                    "color": "default"
                }
            }
            res = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS, json=body)
            if res.status_code == 200:
                print(f"  ✅ 콜아웃 통일 완료")
            else:
                print(f"  ❌ 콜아웃 오류: {res.json().get('message','')}")

        # heading_1 → 검정색
        elif block_type == "heading_1":
            body = {
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": block["heading_1"]["rich_text"][0]["plain_text"] if block["heading_1"]["rich_text"] else ""},
                            "annotations": {"color": "default"}
                        }
                    ]
                }
            }
            res = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS, json=body)
            if res.status_code == 200:
                print(f"  ✅ heading_1 통일 완료")

        # heading_2 → 검정색
        elif block_type == "heading_2":
            body = {
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": block["heading_2"]["rich_text"][0]["plain_text"] if block["heading_2"]["rich_text"] else ""},
                            "annotations": {"color": "default"}
                        }
                    ]
                }
            }
            res = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS, json=body)
            if res.status_code == 200:
                print(f"  ✅ heading_2 통일 완료")

if __name__ == "__main__":
    pages = {
        "📖 이론 학습 가이드":      "357d229a-1c28-81d5-bd35-c850439642c1",
        "💻 SQL 실습 가이드":       "357d229a-1c28-816e-8e82-efc6d59a15d7",
        "❓ 문제풀이 가이드":        "357d229a-1c28-81b6-925a-f5d17323981b",
        "🔁 복습 스케줄 가이드":    "357d229a-1c28-81c4-a768-d2e81d70ce00",
        "📅 학습 계획 가이드":      "357d229a-1c28-81ac-af56-f8b801cff264",
        "🃏 키워드 플래시카드":     "357d229a-1c28-8150-be09-f1848e33d376",
        "❌ 기출문제 오답 패턴":    "357d229a-1c28-8120-8aee-ef3e6874b6f5",
        "📖 SQL 문법 레퍼런스 북":  "357d229a-1c28-81a1-89c6-dbbb4e0d3e11",
    }

    print("=" * 50)
    print("🎨 톤앤매너 통일 시작!")
    print("=" * 50)

    for name, page_id in pages.items():
        unify_page(page_id, name)

    print("\n" + "=" * 50)
    print("🎉 모든 페이지 통일 완료!")
    print("=" * 50)