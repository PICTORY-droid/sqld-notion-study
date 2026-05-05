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

def create_wrong_pattern_page():
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "❌"},
        "properties": {
            "title": {"title": [{"text": {"content": "❌ 기출문제 오답 패턴 분석"}}]}
        },
        "children": [
            {
                "object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": "❌ 기출문제 오답 패턴 분석"}}]}
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "📌 작성 방법\n\n① 문제를 풀다가 틀린 문제가 나오면 바로 여기에 기록하세요.\n② '새 페이지' 버튼 클릭\n③ 문제번호, 틀린 이유 유형 선택, 내용 입력\n④ 단원 반드시 선택\n⑤ 같은 유형 실수가 반복되면 '반복실수' 체크 ✅\n\n💡 틀린 이유 유형 설명\n개념 이해 부족 → 몰라서 틀린 경우\n문제 오독 → 문제를 잘못 읽어서 틀린 경우\n계산 실수 → 알았는데 실수한 경우\n헷갈리는 용어 → 비슷한 용어를 혼동한 경우"}}],
                    "icon": {"type": "emoji", "emoji": "📌"},
                    "color": "red_background"
                }
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "🔁 활용 팁\n시험 1주일 전 → '반복실수' 체크된 것만 필터해서 집중 복습\n틀린 이유 유형별로 필터 → 내 약점 패턴 파악\n개념 이해 부족이 많으면 → 해당 단원 교재 다시 읽기"}}],
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
        "icon": {"type": "emoji", "emoji": "❌"},
        "title": [{"type": "text", "text": {"content": "❌ 오답 패턴 DB"}}],
        "properties": {
            "문제번호":    {"title": {}},
            "틀린내용":    {"rich_text": {}},
            "정답해설":    {"rich_text": {}},
            "틀린이유": {
                "select": {
                    "options": [
                        {"name": "개념 이해 부족", "color": "red"},
                        {"name": "문제 오독",       "color": "orange"},
                        {"name": "계산 실수",       "color": "yellow"},
                        {"name": "헷갈리는 용어",  "color": "purple"},
                    ]
                }
            },
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
            "반복실수": {"checkbox": {}},
        }
    }
    db_res = requests.post("https://api.notion.com/v1/databases", headers=HEADERS, json=db_body)
    if db_res.status_code == 200:
        print(f"  ✅ 오답 패턴 DB 생성 완료!")
        print(f"  🔗 {page_url}")
    else:
        print(f"  ❌ DB 오류: {db_res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 50)
    print("❌ 기출문제 오답 패턴 분석 생성 시작!")
    print("=" * 50)
    create_wrong_pattern_page()
    print("=" * 50)
    print("🎉 완료! 노션에서 확인하세요!")
    print("=" * 50)