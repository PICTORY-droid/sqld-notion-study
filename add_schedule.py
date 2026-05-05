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

# 기간 설정
START_DATE = date(2026, 5, 6)
END_DATE   = date(2026, 8, 21)

# 단계별 구간
def get_phase(d):
    if d <= date(2026, 6, 15):
        return "1단계 - 기초 다지기", "이론학습", "green"
    elif d <= date(2026, 7, 19):
        return "2단계 - SQL 심화", "SQL실습", "blue"
    else:
        return "3단계 - 최종 마무리", "복습", "red"

def add_plan(target_date, phase, study_type):
    url  = f"https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": PLAN_DB},
        "properties": {
            "학습목표": {
                "title": [{"text": {"content": f"[{phase}] {target_date.strftime('%m/%d')} 학습"}}]
            },
            "학습날짜": {
                "date": {"start": target_date.isoformat()}
            },
            "유형": {
                "select": {"name": study_type}
            },
            "완료": {
                "checkbox": False
            }
        }
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"  ✅ {target_date} [{phase}] 추가 완료")
    else:
        print(f"  ❌ {target_date} 오류: {res.json().get('message','')}")

print("=" * 50)
print("📅 학습 계획 자동 입력 시작!")
print(f"   {START_DATE} ~ {END_DATE}")
print("=" * 50)

current = START_DATE
count = 0
while current <= END_DATE:
    phase, study_type, _ = get_phase(current)
    add_plan(current, phase, study_type)
    current += timedelta(days=1)
    count += 1

print("\n" + "=" * 50)
print(f"🎉 총 {count}일 일정 입력 완료!")
print("=" * 50)