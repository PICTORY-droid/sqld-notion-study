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

def create_sql_reference_page():
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "📖"},
        "properties": {
            "title": {"title": [{"text": {"content": "📖 SQL 문법 레퍼런스 북"}}]}
        },
        "children": [
            {
                "object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": "📖 SQL 문법 레퍼런스 북"}}]}
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "📌 작성 방법\n\n① 공부하다가 헷갈리거나 중요한 SQL 문법이 나오면 바로 기록하세요.\n② '새 페이지' 버튼 클릭\n③ 문법이름 입력 → 유형 선택 → 코드 입력 → 설명 작성\n④ 시험에 자주 나오는 것은 '자주출제' 체크 ✅\n\n💡 예시\n문법이름: GROUP BY\n유형: 집계함수\n코드: SELECT 컬럼, COUNT(*) FROM 테이블 GROUP BY 컬럼;\n설명: 특정 컬럼을 기준으로 데이터를 그룹화할 때 사용"}}],
                    "icon": {"type": "emoji", "emoji": "📌"},
                    "color": "green_background"
                }
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "🔁 활용 팁\n시험 전날 → '자주출제' 체크된 것만 필터해서 최종 점검\n유형별 필터 → JOIN / 서브쿼리 등 취약한 유형만 집중 복습\n코드를 직접 손으로 써보면 암기 효과 2배!"}}],
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
        "icon": {"type": "emoji", "emoji": "📖"},
        "title": [{"type": "text", "text": {"content": "📖 SQL 레퍼런스 DB"}}],
        "properties": {
            "문법이름":  {"title": {}},
            "코드":      {"rich_text": {}},
            "설명":      {"rich_text": {}},
            "유형": {
                "select": {
                    "options": [
                        {"name": "SELECT / FROM",  "color": "blue"},
                        {"name": "WHERE 조건",     "color": "green"},
                        {"name": "JOIN",            "color": "orange"},
                        {"name": "집계함수",        "color": "purple"},
                        {"name": "서브쿼리",        "color": "red"},
                        {"name": "DDL",             "color": "gray"},
                        {"name": "DML",             "color": "brown"},
                        {"name": "DCL / TCL",       "color": "pink"},
                    ]
                }
            },
            "자주출제": {"checkbox": {}},
        }
    }
    db_res = requests.post("https://api.notion.com/v1/databases", headers=HEADERS, json=db_body)
    if db_res.status_code == 200:
        print(f"  ✅ SQL 레퍼런스 DB 생성 완료!")
        print(f"  🔗 {page_url}")
    else:
        print(f"  ❌ DB 오류: {db_res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 50)
    print("📖 SQL 문법 레퍼런스 북 생성 시작!")
    print("=" * 50)
    create_sql_reference_page()
    print("=" * 50)
    print("🎉 완료! 노션에서 확인하세요!")
    print("=" * 50)