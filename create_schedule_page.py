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

def create_schedule_page():
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "📅"},
        "properties": {
            "title": {"title": [{"text": {"content": "📅 학습 계획 가이드"}}]}
        },
        "children": [
            {
                "object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": "📅 학습 계획 가이드"}}]}
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "📌 학습 계획 DB가 뭐예요?\n\n매일 공부할 내용을 미리 계획하고 기록하는 공간이에요!\n오늘 뭘 공부했는지, 얼마나 공부했는지 기록해두면\n시험까지 체계적으로 준비할 수 있어요 😊\n\n학습 단계는 3단계로 나눠져 있어요!\n1단계 - 기초 다지기 (~ 6월 15일) → 이론학습\n2단계 - SQL 심화 (~ 7월 19일) → SQL실습\n3단계 - 최종 마무리 (~ 8월 21일) → 복습"}}],
                    "icon": {"type": "emoji", "emoji": "📅"},
                    "color": "blue_background"
                }
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "📌 작성 방법\n\n학습 계획 DB는 이미 자동으로 날짜별 계획이 들어가 있어요!\n매일 공부하고 나서 아래 항목들을 직접 체크하면 돼요!\n\n① 완료 체크 ✅\n공부 끝나면 완료 체크 눌러주세요!\n\n② 목표시간_분\n오늘 몇 분 공부할 계획인지 숫자로 입력하세요\n예) 60 → 1시간 공부 계획\n\n③ 실제시간_분\n실제로 몇 분 공부했는지 숫자로 입력하세요\n예) 45 → 45분 공부함\n\n④ 오늘의메모\n오늘 공부하면서 느낀 점이나 특이사항을 써주세요\n예) GROUP BY 개념이 헷갈림. 내일 다시 볼 것!"}}],
                    "icon": {"type": "emoji", "emoji": "📌"},
                    "color": "green_background"
                }
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "🔁 유형 설명\n\n유형은 오늘 어떤 공부를 했는지 구분하는 거예요!\n\n이론학습 → 교재 읽고 개념 공부한 날\nSQL실습 → SQL 문법 직접 써보면서 공부한 날\n문제풀이 → 기출문제나 연습문제 푼 날\n복습 → 전에 공부한 내용 다시 본 날\n오답정리 → 틀린 문제 다시 정리한 날"}}],
                    "icon": {"type": "emoji", "emoji": "🔁"},
                    "color": "yellow_background"
                }
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "💡 활용 팁\n\n매일 공부 시작할 때 → 학습 계획 DB 열어서 오늘 날짜 확인!\n매일 공부 끝날 때 → 완료 체크 + 실제시간 + 오늘의메모 입력!\n\n목표시간보다 실제시간이 적으면 → 내일 더 열심히!\n목표시간보다 실제시간이 많으면 → 잘하고 있어요! 😊"}}],
                    "icon": {"type": "emoji", "emoji": "💡"},
                    "color": "purple_background"
                }
            },
            {"object": "block", "type": "divider", "divider": {}},
            {
                "object": "block", "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "🎯 예시 — 오늘 공부 기록하는 법"}}]}
            },
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "예시 1) 오늘 이론공부 1시간 한 경우\n\n학습목표: [1단계 - 기초 다지기] 05/06 학습\n유형: 이론학습\n목표시간_분: 60\n실제시간_분: 55\n완료: ✅\n오늘의메모: 엔터티, 속성, 관계 개념 공부함. 식별자 부분이 헷갈림!\n\n예시 2) 오늘 SQL 실습 30분 한 경우\n\n학습목표: [2단계 - SQL 심화] 07/01 학습\n유형: SQL실습\n목표시간_분: 60\n실제시간_분: 30\n완료: ✅\n오늘의메모: GROUP BY, HAVING 실습함. 시간이 부족해서 내일 이어서 할 것!"}}],
                    "icon": {"type": "emoji", "emoji": "🎯"},
                    "color": "gray_background"
                }
            },
        ]
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code != 200:
        print(f"❌ 페이지 오류: {res.json().get('message','')}")
        return

    page_url = res.json().get("url", "")
    print(f"✅ 페이지 생성 완료!")
    print(f"🔗 {page_url}")

if __name__ == "__main__":
    print("=" * 50)
    print("📅 학습 계획 가이드 페이지 생성 시작!")
    print("=" * 50)
    create_schedule_page()
    print("=" * 50)
    print("🎉 완료! 노션에서 확인하세요!")
    print("=" * 50)