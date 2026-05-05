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

def create_flashcard_page():
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🃏"},
        "properties": {
            "title": {"title": [{"text": {"content": "🃏 키워드 플래시카드"}}]}
        },
        "children": [
            {
                "object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": "🃏 키워드 플래시카드"}}]}
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "📌 작성 방법\n\n① 오늘 공부하다가 외워야 할 용어가 나오면 바로 여기 추가하세요.\n② 오른쪽 위 '새 페이지' 버튼 클릭\n③ 키워드(앞면) → 질문 → 답(뒷면) 순서로 입력\n④ 단원과 난이도 반드시 선택\n⑤ 외웠으면 '암기완료' 체크 ✅\n\n💡 예시\n키워드: 엔터티(Entity)\n질문: 엔터티란 무엇인가?\n답: 현실 세계에서 독립적으로 존재하는 사람, 사물, 개념 등의 집합\n단원: 1과목 - 데이터 모델링\n난이도: ⭐ 쉬움"}}],
                    "icon": {"type": "emoji", "emoji": "📌"},
                    "color": "blue_background"
                }
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "🔁 활용 팁\n시험 3일 전 → 암기완료 체크 안 된 것만 필터해서 집중 암기\n시험 전날 → 난이도 ⭐⭐⭐ 어려움만 필터해서 최종 점검"}}],
                    "icon": {"type": "emoji", "emoji": "🔁"},
                    "color": "yellow_background"
                }
            },
            {"object": "block", "type": "divider", "divider": {}},
        ]
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code != 200:
        print(f"  ❌ 페이지 오류: {res.json().get('message','')}")
        return

    page_id  = res.json()["id"]
    page_url = res.json().get("url", "")
    print(f"  ✅ 페이지 생성 완료!")

    db_body = {
        "parent": {"type": "page_id", "page_id": page_id},
        "icon": {"type": "emoji", "emoji": "🃏"},
        "title": [{"type": "text", "text": {"content": "🃏 플래시카드 DB"}}],
        "properties": {
            "키워드":   {"title": {}},
            "질문":     {"rich_text": {}},
            "답":       {"rich_text": {}},
            "단원": {
                "select": {
                    "options": [
                        {"name": "1과목 - 데이터 모델링의 이해", "color": "green"},
                        {"name": "1과목 - 데이터 모델과 SQL",    "color": "blue"},
                        {"name": "2과목 - SQL 기본",              "color": "blue"},
                        {"name": "2과목 - SQL 활용",              "color": "purple"},
                        {"name": "2과목 - 관리 구문",             "color": "orange"},
                    ]
                }
            },
            "난이도": {
                "select": {
                    "options": [
                        {"name": "⭐ 쉬움",       "color": "green"},
                        {"name": "⭐⭐ 보통",     "color": "yellow"},
                        {"name": "⭐⭐⭐ 어려움", "color": "red"},
                    ]
                }
            },
            "암기완료": {"checkbox": {}},
        }
    }
    db_res = requests.post("https://api.notion.com/v1/databases", headers=HEADERS, json=db_body)
    if db_res.status_code == 200:
        print(f"  ✅ 플래시카드 DB 생성 완료!")
        print(f"  🔗 {page_url}")
    else:
        print(f"  ❌ DB 오류: {db_res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 50)
    print("🃏 키워드 플래시카드 생성 시작!")
    print("=" * 50)
    create_flashcard_page()
    print("=" * 50)
    print("🎉 완료! 노션에서 확인하세요!")
    print("=" * 50)