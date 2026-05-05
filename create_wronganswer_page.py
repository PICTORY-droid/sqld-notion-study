import requests
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN   = os.getenv("NOTION_TOKEN")
PARENT_PAGE_ID = os.getenv("PARENT_PAGE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_wronganswer_page():
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "📝"},
        "properties": {
            "title": {"title": [{"text": {"content": "📝 오답 노트"}}]}
        },
        "children": [
            {
                "object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": "📝 오답 노트"}}]}
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "📌 작성 방법\n\n① Git Bash 열기\n② 아래 명령어 복사해서 붙여넣기\n\npython add_wronganswer.py \"오답항목\" \"틀린날짜\" \"틀린이유\" \"오답메모\"\n\n③ 틀린이유는 아래 중 하나를 그대로 복사하세요!\n\n개념을 몰랐음  ← 배운 적 없거나 몰라서 틀린 경우\n문제를 잘못 읽음  ← 문제를 제대로 안 읽어서 틀린 경우\n헷갈리는 개념  ← 비슷한 개념이 헷갈려서 틀린 경우\n계산 실수  ← 알았는데 실수한 경우\n시간 부족  ← 시간이 없어서 제대로 못 푼 경우\n\n💡 예시\npython add_wronganswer.py \"NULL 비교 문제\" \"2026-05-06\" \"개념을 몰랐음\" \"NULL은 IS NULL로 비교해야 함\""}}],
                    "icon": {"type": "emoji", "emoji": "📌"},
                    "color": "red_background"
                }
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "🔁 활용 팁\n\n재풀이 후 노션에서 직접 체크하세요!\n✅ 재풀이완료 체크 → 재풀이날짜 입력 → 재풀이결과 선택\n❌ 또 틀렸으면 → 오답메모에 추가로 정리하기!"}}],
                    "icon": {"type": "emoji", "emoji": "🔁"},
                    "color": "yellow_background"
                }
            },
            {"object": "block", "type": "divider", "divider": {}},
        ]
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code != 200:
        print(f"❌ 페이지 오류: {res.json().get('message','')}")
        return

    page_id  = res.json()["id"]
    page_url = res.json().get("url", "")
    print(f"✅ 페이지 생성 완료!")
    print(f"🔗 {page_url}")

if __name__ == "__main__":
    print("=" * 50)
    print("📝 오답 노트 페이지 생성 시작!")
    print("=" * 50)
    create_wronganswer_page()
    print("=" * 50)
    print("🎉 완료! 노션에서 확인하세요!")
    print("=" * 50)