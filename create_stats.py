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

PLAN_DB        = "357d229a-1c28-81d0-b594-c3ff7c081a26"
THEORY_DB      = "357d229a-1c28-81e9-a858-ca17697f7429"
REVIEW_DB      = "357d229a-1c28-8168-9d60-cd4d3379cc93"
QUIZ_DB        = "357d229a-1c28-816d-b080-c10b7b4cc44e"
WRONGANSWER_DB = "357d229a-1c28-8186-ba13-f81e4159f1e4"

today = date.today()
exam  = date(2026, 8, 22)
start = date(2026, 5, 6)
dday  = (exam - today).days
elapsed = (today - start).days + 1
total = 108
progress = round((elapsed / total) * 100, 1)

def count_checked(db_id, prop):
    url  = f"https://api.notion.com/v1/databases/{db_id}/query"
    body = {"filter": {"property": prop, "checkbox": {"equals": True}}}
    res  = requests.post(url, headers=HEADERS, json=body)
    return len(res.json().get("results", []))

def count_all(db_id):
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    res = requests.post(url, headers=HEADERS, json={})
    return len(res.json().get("results", []))

print("📊 통계 계산 중...")
plan_done    = count_checked(PLAN_DB, "완료")
plan_total   = count_all(PLAN_DB)
theory_done  = count_checked(THEORY_DB, "완료")
theory_total = count_all(THEORY_DB)
review_done  = count_checked(REVIEW_DB, "1차복습_완료")
review_total = count_all(REVIEW_DB)
quiz_total   = count_all(QUIZ_DB)
wrong_total  = count_all(WRONGANSWER_DB)
wrong_done   = count_checked(WRONGANSWER_DB, "재풀이완료")

def make_bar(done, total):
    if total == 0:
        return "시작 전"
    pct = round(done / total * 100)
    filled = pct // 10
    bar = "█" * filled + "░" * (10 - filled)
    return f"{bar} {pct}%"

def create_stats_page():
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "📊"},
        "properties": {
            "title": {"title": [{"text": {"content": "📊 진도율 통계"}}]}
        },
        "children": [
            # 제목
            {
                "object": "block", "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": "📊 SQLD 학습 진도율 통계"}}]}
            },
            # D-day 콜아웃
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": f"🎯 시험까지 D-{dday}일  |  전체 진도 {progress}%  |  경과 {elapsed}일 / 108일"}}],
                    "icon": {"type": "emoji", "emoji": "⏳"},
                    "color": "yellow_background"
                }
            },
            {"object": "block", "type": "divider", "divider": {}},
            # 전체 진도 섹션
            {
                "object": "block", "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "📅 학습 계획 달성률"}}]}
            },
            {
                "object": "block", "type": "table",
                "table": {
                    "table_width": 4,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "항목"}}],
                                [{"type": "text", "text": {"content": "완료"}}],
                                [{"type": "text", "text": {"content": "전체"}}],
                                [{"type": "text", "text": {"content": "진도율"}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "📅 학습 계획"}}],
                                [{"type": "text", "text": {"content": str(plan_done)}}],
                                [{"type": "text", "text": {"content": str(plan_total)}}],
                                [{"type": "text", "text": {"content": make_bar(plan_done, plan_total)}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "📖 이론 학습"}}],
                                [{"type": "text", "text": {"content": str(theory_done)}}],
                                [{"type": "text", "text": {"content": str(theory_total)}}],
                                [{"type": "text", "text": {"content": make_bar(theory_done, theory_total)}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "🔁 복습 완료"}}],
                                [{"type": "text", "text": {"content": str(review_done)}}],
                                [{"type": "text", "text": {"content": str(review_total)}}],
                                [{"type": "text", "text": {"content": make_bar(review_done, review_total)}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "❓ 문제풀이"}}],
                                [{"type": "text", "text": {"content": str(quiz_total)}}],
                                [{"type": "text", "text": {"content": "—"}}],
                                [{"type": "text", "text": {"content": f"총 {quiz_total}문제 풀이"}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "📝 오답 재풀이"}}],
                                [{"type": "text", "text": {"content": str(wrong_done)}}],
                                [{"type": "text", "text": {"content": str(wrong_total)}}],
                                [{"type": "text", "text": {"content": make_bar(wrong_done, wrong_total)}}],
                            ]}
                        },
                    ]
                }
            },
            {"object": "block", "type": "divider", "divider": {}},
            # 단계별 현황
            {
                "object": "block", "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "🗓️ 단계별 현황"}}]}
            },
            {
                "object": "block", "type": "table",
                "table": {
                    "table_width": 4,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "단계"}}],
                                [{"type": "text", "text": {"content": "기간"}}],
                                [{"type": "text", "text": {"content": "일수"}}],
                                [{"type": "text", "text": {"content": "상태"}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "🟢 1단계 기초"}}],
                                [{"type": "text", "text": {"content": "5/6 ~ 6/15"}}],
                                [{"type": "text", "text": {"content": "41일"}}],
                                [{"type": "text", "text": {"content": "🔥 진행중" if today <= date(2026,6,15) else "✅ 완료"}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "🔵 2단계 SQL"}}],
                                [{"type": "text", "text": {"content": "6/16 ~ 7/19"}}],
                                [{"type": "text", "text": {"content": "34일"}}],
                                [{"type": "text", "text": {"content": "🔥 진행중" if date(2026,6,16) <= today <= date(2026,7,19) else ("✅ 완료" if today > date(2026,7,19) else "⏳ 예정")}}],
                            ]}
                        },
                        {
                            "object": "block", "type": "table_row",
                            "table_row": {"cells": [
                                [{"type": "text", "text": {"content": "🔴 3단계 마무리"}}],
                                [{"type": "text", "text": {"content": "7/25 ~ 8/21"}}],
                                [{"type": "text", "text": {"content": "28일"}}],
                                [{"type": "text", "text": {"content": "🔥 진행중" if date(2026,7,25) <= today <= date(2026,8,21) else ("✅ 완료" if today > date(2026,8,21) else "⏳ 예정")}}],
                            ]}
                        },
                    ]
                }
            },
            {"object": "block", "type": "divider", "divider": {}},
            {
                "object": "block", "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "💡 이 페이지는 python create_stats.py 를 실행할 때마다 새로 만들어져요. 주기적으로 실행해서 진도를 확인하세요!"}}],
                    "icon": {"type": "emoji", "emoji": "💡"},
                    "color": "gray_background"
                }
            },
        ]
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"  ✅ 진도율 통계 페이지 생성 완료!")
        print(f"  🔗 {res.json().get('url','')}")
    else:
        print(f"  ❌ 오류: {res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 50)
    print("📊 진도율 통계 페이지 생성 시작!")
    print("=" * 50)
    create_stats_page()
    print("=" * 50)
    print("🎉 완료! 노션에서 확인하세요!")
    print("=" * 50)