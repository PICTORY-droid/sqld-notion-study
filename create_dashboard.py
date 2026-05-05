import requests
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN   = os.getenv("NOTION_TOKEN")
PARENT_PAGE_ID = os.getenv("PARENT_PAGE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# DB ID 목록
THEORY_DB      = "357d229a-1c28-81e9-a858-ca17697f7429"
SQL_DB         = "357d229a-1c28-8126-ba08-e099b68a2cf3"
REVIEW_DB      = "357d229a-1c28-8168-9d60-cd4d3379cc93"
QUIZ_DB        = "357d229a-1c28-816d-b080-c10b7b4cc44e"
WRONGANSWER_DB = "357d229a-1c28-8186-ba13-f81e4159f1e4"
PLAN_DB        = "357d229a-1c28-81d0-b594-c3ff7c081a26"

# D-day 계산
today   = date.today()
exam    = date(2026, 8, 22)
dday    = (exam - today).days

def create_dashboard():
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon":   {"type": "emoji", "emoji": "🏠"},
        "properties": {
            "title": {"title": [{"text": {"content": "🏠 메인 대시보드"}}]}
        },
        "children": [
            # 헤더
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": "📚 SQLD 합격 프로젝트"}}]}
            },
            # D-day
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": f"⏳ 시험까지 D-{dday}일  |  시험일: 2026년 8월 22일  |  오늘: {today.strftime('%Y년 %m월 %d일')}"}}],
                    "icon": {"type": "emoji", "emoji": "🎯"},
                    "color": "red_background"
                }
            },
            # 구분선
            {"object": "block", "type": "divider", "divider": {}},
            # 3단계 안내
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "📅 학습 3단계 로드맵"}}]}
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "1단계 기초 다지기: 5월 6일 ~ 6월 15일 (41일)\n이론 위주, 용어와 개념 익히기"}}],
                    "icon": {"type": "emoji", "emoji": "🟢"},
                    "color": "green_background"
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "2단계 SQL 심화: 6월 16일 ~ 7월 19일 (34일)\nSQL 실습 + 기출문제 시작"}}],
                    "icon": {"type": "emoji", "emoji": "🔵"},
                    "color": "blue_background"
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "3단계 최종 마무리: 7월 25일 ~ 8월 21일 (28일)\n오답 정리 + 기출 반복 + 복습 총가동"}}],
                    "icon": {"type": "emoji", "emoji": "🔴"},
                    "color": "red_background"
                }
            },
            # 구분선
            {"object": "block", "type": "divider", "divider": {}},
            # DB 바로가기
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "🗂️ DB 바로가기"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": "📖 이론 학습 DB — 단원별 개념 정리"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": "💻 SQL 실습 DB — SQL 문법 직접 써보기"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": "🔁 복습 스케줄 DB — 에빙하우스 망각곡선 복습"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": "❓ 문제풀이 DB — 기출문제 풀기"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": "📝 오답 노트 DB — 틀린 문제 모아보기"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": "📅 학습 계획 DB — 날짜별 학습 기록"}}]}
            },
            # 구분선
            {"object": "block", "type": "divider", "divider": {}},
            # 복습 스크립트 안내
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "💡 매일 공부 후 할 일"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"text": {"content": "학습 계획 DB에서 오늘 날짜 열기 → 완료 체크 ✅"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"text": {"content": "이론 학습 DB에 오늘 공부한 단원 기록"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"text": {"content": "Git Bash에서 python add_review.py 실행 → 복습 날짜 자동 등록"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"text": {"content": "문제 풀었으면 문제풀이 DB에 결과 기록"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"text": {"content": "틀린 문제는 오답 노트 DB에 기록"}}]}
            },
        ]
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        page_url = res.json().get("url", "")
        print(f"  ✅ 메인 대시보드 생성 완료!")
        print(f"  🔗 {page_url}")
    else:
        print(f"  ❌ 오류: {res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 50)
    print("🏠 메인 대시보드 생성 시작!")
    print("=" * 50)
    create_dashboard()
    print("=" * 50)
    print("🎉 완료! 노션에서 확인하세요!")
    print("=" * 50)