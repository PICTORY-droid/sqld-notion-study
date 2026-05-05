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

def create_database(parent_id, title, properties):
    url  = "https://api.notion.com/v1/databases"
    body = {
        "parent":     {"type": "page_id", "page_id": parent_id},
        "title":      [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"  ✅ '{title}' 생성 완료!")
        return res.json()["id"]
    else:
        print(f"  ❌ 오류: {res.status_code} → {res.json().get('message','')}")
        return None

def create_theory_db(parent_id):
    print("\n📖 이론 학습 DB 만드는 중...")
    return create_database(parent_id, "📖 이론 학습 DB", {
        "단원명":    {"title": {}},
        "과목":      {"select": {"options": [
                        {"name": "1과목 - 데이터 모델링", "color": "green"},
                        {"name": "2과목 - SQL 기본 및 활용", "color": "blue"},
                    ]}},
        "학습일":    {"date": {}},
        "이해도":    {"select": {"options": [
                        {"name": "⭐ 잘 모름",      "color": "red"},
                        {"name": "⭐⭐ 조금 앎",    "color": "orange"},
                        {"name": "⭐⭐⭐ 보통",     "color": "yellow"},
                        {"name": "⭐⭐⭐⭐ 잘 앎",  "color": "green"},
                        {"name": "⭐⭐⭐⭐⭐ 완벽", "color": "blue"},
                    ]}},
        "핵심키워드": {"multi_select": {"options": []}},
        "복습필요":  {"checkbox": {}},
        "완료":      {"checkbox": {}},
    })

def create_sql_db(parent_id):
    print("\n💻 SQL 실습 DB 만드는 중...")
    return create_database(parent_id, "💻 SQL 실습 DB", {
        "문법명":   {"title": {}},
        "분류":     {"select": {"options": [
                        {"name": "SELECT (조회)",     "color": "blue"},
                        {"name": "WHERE (조건)",      "color": "green"},
                        {"name": "JOIN (연결)",       "color": "purple"},
                        {"name": "GROUP BY (그룹)",  "color": "orange"},
                        {"name": "서브쿼리",          "color": "pink"},
                        {"name": "윈도우함수",        "color": "yellow"},
                        {"name": "DDL (테이블 생성)", "color": "gray"},
                        {"name": "DML (데이터 조작)", "color": "red"},
                    ]}},
        "실습일":   {"date": {}},
        "난이도":   {"select": {"options": [
                        {"name": "쉬움",   "color": "green"},
                        {"name": "보통",   "color": "yellow"},
                        {"name": "어려움", "color": "red"},
                    ]}},
        "오류발생": {"checkbox": {}},
        "오류원인": {"rich_text": {}},
        "완료":     {"checkbox": {}},
    })

def create_review_db(parent_id):
    print("\n🔁 복습 스케줄 DB 만드는 중...")
    return create_database(parent_id, "🔁 복습 스케줄 DB", {
        "복습항목":      {"title": {}},
        "최초학습일":    {"date": {}},
        "1일후_복습일":  {"date": {}},
        "3일후_복습일":  {"date": {}},
        "7일후_복습일":  {"date": {}},
        "30일후_복습일": {"date": {}},
        "1차복습_완료":  {"checkbox": {}},
        "2차복습_완료":  {"checkbox": {}},
        "3차복습_완료":  {"checkbox": {}},
        "4차복습_완료":  {"checkbox": {}},
        "복습메모":      {"rich_text": {}},
    })

def create_quiz_db(parent_id):
    print("\n❓ 문제풀이 DB 만드는 중...")
    return create_database(parent_id, "❓ 문제풀이 DB", {
        "문제명":       {"title": {}},
        "출처":         {"select": {"options": [
                            {"name": "이기적 교재",  "color": "green"},
                            {"name": "기출문제",     "color": "blue"},
                            {"name": "모의고사",     "color": "purple"},
                            {"name": "인터넷 문제",  "color": "orange"},
                        ]}},
        "과목":         {"select": {"options": [
                            {"name": "1과목", "color": "green"},
                            {"name": "2과목", "color": "blue"},
                        ]}},
        "풀이날짜":     {"date": {}},
        "정답여부":     {"select": {"options": [
                            {"name": "✅ 정답",  "color": "green"},
                            {"name": "❌ 오답",  "color": "red"},
                            {"name": "🤔 찍음", "color": "orange"},
                        ]}},
        "난이도":       {"select": {"options": [
                            {"name": "쉬움",   "color": "green"},
                            {"name": "보통",   "color": "yellow"},
                            {"name": "어려움", "color": "red"},
                        ]}},
        "오답노트작성": {"checkbox": {}},
    })

def create_wronganswer_db(parent_id):
    print("\n📝 오답 노트 DB 만드는 중...")
    return create_database(parent_id, "📝 오답 노트 DB", {
        "오답항목":  {"title": {}},
        "틀린날짜":  {"date": {}},
        "틀린이유":  {"select": {"options": [
                        {"name": "개념을 몰랐음",    "color": "red"},
                        {"name": "문제를 잘못 읽음", "color": "orange"},
                        {"name": "헷갈리는 개념",    "color": "purple"},
                        {"name": "계산 실수",        "color": "yellow"},
                        {"name": "시간 부족",        "color": "gray"},
                    ]}},
        "재풀이완료": {"checkbox": {}},
        "재풀이날짜": {"date": {}},
        "재풀이결과": {"select": {"options": [
                        {"name": "✅ 이번엔 맞음", "color": "green"},
                        {"name": "❌ 또 틀림",    "color": "red"},
                    ]}},
        "오답메모":  {"rich_text": {}},
    })

def create_plan_db(parent_id):
    print("\n📅 학습 계획 DB 만드는 중...")
    return create_database(parent_id, "📅 학습 계획 DB", {
        "학습목표":    {"title": {}},
        "학습날짜":    {"date": {}},
        "유형":        {"select": {"options": [
                            {"name": "이론학습",  "color": "green"},
                            {"name": "SQL실습",  "color": "blue"},
                            {"name": "문제풀이", "color": "purple"},
                            {"name": "복습",     "color": "orange"},
                            {"name": "오답정리", "color": "red"},
                        ]}},
        "목표시간_분": {"number": {"format": "number"}},
        "실제시간_분": {"number": {"format": "number"}},
        "완료":        {"checkbox": {}},
        "오늘의메모":  {"rich_text": {}},
    })

if __name__ == "__main__":
    print("=" * 50)
    print("📚 SQLD 노션 학습 시스템 자동 생성 시작!")
    print("=" * 50)

    if not NOTION_TOKEN or "여기에" in NOTION_TOKEN:
        print("\n⚠️  .env 파일에 NOTION_TOKEN을 먼저 입력해주세요!")
        print("   발급 주소: https://www.notion.so/my-integrations")
        exit()

    create_theory_db(PARENT_PAGE_ID)
    create_sql_db(PARENT_PAGE_ID)
    create_review_db(PARENT_PAGE_ID)
    create_quiz_db(PARENT_PAGE_ID)
    create_wronganswer_db(PARENT_PAGE_ID)
    create_plan_db(PARENT_PAGE_ID)

    print("\n" + "=" * 50)
    print("🎉 모든 DB 생성 완료! 노션을 확인해보세요!")
    print("=" * 50)