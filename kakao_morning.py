import requests
import os
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN       = os.getenv("NOTION_TOKEN")
KAKAO_ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN")
KAKAO_REFRESH_TOKEN= os.getenv("KAKAO_REFRESH_TOKEN")
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

PLAN_DB = "357d229a-1c28-81d0-b594-c3ff7c081a26"

HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def refresh_kakao_token():
    res = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type":    "refresh_token",
            "client_id":     KAKAO_REST_API_KEY,
            "refresh_token": KAKAO_REFRESH_TOKEN,
        }
    )
    if res.status_code == 200:
        return res.json().get("access_token")
    return KAKAO_ACCESS_TOKEN

def send_kakao(message):
    import json
    token = refresh_kakao_token()
    template = {
        "object_type": "text",
        "text": message,
        "link": {
            "web_url": "https://notion.so",
            "mobile_web_url": "https://notion.so"
        }
    }
    res = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers={"Authorization": f"Bearer {token}"},
        data={"template_object": json.dumps(template, ensure_ascii=False)}
    )
    if res.status_code == 200:
        print("✅ 카톡 전송 완료!")
    else:
        print(f"❌ 카톡 전송 실패: {res.json()}")

def get_yesterday_done():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    url  = f"https://api.notion.com/v1/databases/{PLAN_DB}/query"
    body = {
        "filter": {
            "property": "학습날짜",
            "date": {"equals": yesterday}
        }
    }
    res  = requests.post(url, headers=HEADERS_NOTION, json=body)
    if res.status_code != 200:
        return None, None
    results = res.json().get("results", [])
    if not results:
        return yesterday, None
    page   = results[0]
    props  = page.get("properties", {})
    목표   = props.get("학습목표", {}).get("title", [{}])
    목표텍스트 = 목표[0].get("plain_text", "") if 목표 else ""
    범위   = props.get("공부범위", {}).get("rich_text", [{}])
    범위텍스트 = 범위[0].get("plain_text", "") if 범위 else ""
    상태   = props.get("상태", {}).get("select", {})
    상태텍스트 = 상태.get("name", "예정") if 상태 else "예정"
    return yesterday, {
        "목표": 목표텍스트,
        "범위": 범위텍스트,
        "상태": 상태텍스트,
    }

def get_today_plan():
    today = date.today().isoformat()
    url   = f"https://api.notion.com/v1/databases/{PLAN_DB}/query"
    body  = {
        "filter": {
            "property": "학습날짜",
            "date": {"equals": today}
        }
    }
    res  = requests.post(url, headers=HEADERS_NOTION, json=body)
    if res.status_code != 200:
        return None
    results = res.json().get("results", [])
    if not results:
        return None
    page   = results[0]
    props  = page.get("properties", {})
    목표   = props.get("학습목표", {}).get("title", [{}])
    목표텍스트 = 목표[0].get("plain_text", "") if 목표 else ""
    범위   = props.get("공부범위", {}).get("rich_text", [{}])
    범위텍스트 = 범위[0].get("plain_text", "") if 범위 else ""
    할일   = props.get("오늘할일", {}).get("rich_text", [{}])
    할일텍스트 = 할일[0].get("plain_text", "") if 할일 else ""
    교재   = props.get("교재페이지", {}).get("rich_text", [{}])
    교재텍스트 = 교재[0].get("plain_text", "") if 교재 else ""
    return {
        "목표": 목표텍스트,
        "범위": 범위텍스트,
        "할일": 할일텍스트,
        "교재": 교재텍스트,
    }

def build_message(yesterday, yesterday_data, today_data):
    today_str     = date.today().strftime("%Y년 %m월 %d일")
    yesterday_str = (date.today() - timedelta(days=1)).strftime("%m월 %d일")

    msg = f"📚 SQLD 학습 알림 | {today_str}\n"
    msg += "=" * 25 + "\n\n"

    msg += f"✅ 어제({yesterday_str}) 공부한 내용\n"
    if yesterday_data:
        상태아이콘 = "✅" if yesterday_data['상태'] == "완료" else "⏳"
        msg += f"{상태아이콘} {yesterday_data['범위']}\n"
        msg += f"📖 {yesterday_data['목표']}\n"
    else:
        msg += "📭 어제 학습 기록이 없어요\n"

    msg += "\n" + "-" * 25 + "\n\n"

    msg += f"🎯 오늘 할 일\n"
    if today_data:
        msg += f"📌 {today_data['범위']}\n"
        msg += f"📝 {today_data['할일']}\n"
        msg += f"📗 교재: {today_data['교재']}\n"
    else:
        msg += "📭 오늘 학습 일정이 없어요\n"

    msg += "\n" + "=" * 25 + "\n"
    msg += "💪 오늘도 파이팅!"
    return msg

if __name__ == "__main__":
    print("📱 카톡 아침 알림 시작!")
    yesterday, yesterday_data = get_yesterday_done()
    today_data                = get_today_plan()
    message                   = build_message(yesterday, yesterday_data, today_data)
    print("\n--- 전송할 메시지 ---")
    print(message)
    print("-------------------\n")
    send_kakao(message)