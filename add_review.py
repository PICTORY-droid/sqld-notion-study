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

REVIEW_DB = "357d229a-1c28-8168-9d60-cd4d3379cc93"

def add_review(topic, study_date):
    d = date.fromisoformat(study_date)
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": REVIEW_DB},
        "properties": {
            "복습항목":      {"title": [{"text": {"content": topic}}]},
            "최초학습일":    {"date": {"start": study_date}},
            "1일후_복습일":  {"date": {"start": (d + timedelta(days=1)).isoformat()}},
            "3일후_복습일":  {"date": {"start": (d + timedelta(days=3)).isoformat()}},
            "7일후_복습일":  {"date": {"start": (d + timedelta(days=7)).isoformat()}},
            "30일후_복습일": {"date": {"start": (d + timedelta(days=30)).isoformat()}},
            "1차복습_완료":  {"checkbox": False},
            "2차복습_완료":  {"checkbox": False},
            "3차복습_완료":  {"checkbox": False},
            "4차복습_완료":  {"checkbox": False},
        }
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"  ✅ [{study_date}] '{topic}' 복습 일정 추가 완료!")
        print(f"     1차: {(d+timedelta(1)).isoformat()} / 2차: {(d+timedelta(3)).isoformat()} / 3차: {(d+timedelta(7)).isoformat()} / 4차: {(d+timedelta(30)).isoformat()}")
    else:
        print(f"  ❌ 오류: {res.json().get('message','')}")

if __name__ == "__main__":
    print("=" * 50)
    print("🔁 복습 스케줄 추가")
    print("=" * 50)
    topic      = input("\n공부한 내용 입력 (예: 데이터 모델링 기본 개념): ").strip()
    study_date = input("공부한 날짜 입력 (예: 2026-05-06): ").strip()
    add_review(topic, study_date)
    print("\n💡 노션 복습 스케줄 DB에서 확인하세요!")