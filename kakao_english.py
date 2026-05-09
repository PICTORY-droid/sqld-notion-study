import requests
import os
import json
import random
from datetime import date
from dotenv import load_dotenv

load_dotenv()
KAKAO_REST_API_KEY  = os.getenv("KAKAO_REST_API_KEY")
KAKAO_REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN")

def get_fresh_token():
    res = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type":    "refresh_token",
            "client_id":     KAKAO_REST_API_KEY,
            "refresh_token": KAKAO_REFRESH_TOKEN,
        }
    )
    data = res.json()
    if "access_token" in data:
        print("✅ 토큰 자동 갱신 완료")
        return data["access_token"]
    print("⚠️ 토큰 갱신 실패, 기존 토큰 사용")
    return os.getenv("KAKAO_ACCESS_TOKEN")

KAKAO_ACCESS_TOKEN = get_fresh_token()

# SQLD 영어단어 A-Z 전체 목록
# abbr: True면 약어 (AVG에버리지 형식), False면 일반 단어 (Attribute(어트리뷰트) 형식)
WORDS = [
    {"word": "Attribute",            "pron": "어트리뷰트",       "abbr": False, "desc": "속성",                    "ex": "엔터티가 가지는 세부 데이터 항목 (예: 이름, 나이)"},
    {"word": "Aggregate Function",   "pron": "애그리게이트 펑션", "abbr": False, "desc": "집계 함수",               "ex": "여러 행을 하나의 결과로 반환 (SUM, AVG, COUNT 등)"},
    {"word": "Association",          "pron": "어소시에이션",      "abbr": False, "desc": "연관 / 관계",             "ex": "두 엔터티 간의 관계를 나타냄"},
    {"word": "Business Rule",        "pron": "비즈니스 룰",       "abbr": False, "desc": "업무 규칙",               "ex": "데이터 모델링의 기반이 되는 업무 요건"},
    {"word": "Cardinality",          "pron": "카디널리티",        "abbr": False, "desc": "집합의 원소 수",           "ex": "1:1, 1:N, M:N 관계를 나타냄"},
    {"word": "Column",               "pron": "컬럼",              "abbr": False, "desc": "열 / 컬럼",               "ex": "테이블에서 세로 방향의 데이터 항목"},
    {"word": "Constraint",           "pron": "컨스트레인트",      "abbr": False, "desc": "제약조건",                "ex": "PK, FK, UNIQUE, NOT NULL 등 데이터 무결성 규칙"},
    {"word": "CRUD",                 "pron": "크루드",            "abbr": True,  "desc": "생성·조회·수정·삭제",     "ex": "Create, Read, Update, Delete의 약자"},
    {"word": "Composite Key",        "pron": "컴포지트 키",       "abbr": False, "desc": "복합키",                  "ex": "두 개 이상의 컬럼으로 이루어진 기본키"},
    {"word": "Cascading",            "pron": "캐스케이딩",        "abbr": False, "desc": "연쇄 처리",               "ex": "부모 행 삭제 시 자식 행도 함께 삭제되는 옵션"},
    {"word": "Data Model",           "pron": "데이터 모델",       "abbr": False, "desc": "데이터 모델",             "ex": "현실 세계 데이터를 추상화해 표현한 구조"},
    {"word": "DDL",                  "pron": "디디엘",            "abbr": True,  "desc": "데이터 정의어",           "ex": "CREATE, ALTER, DROP 등 구조를 정의하는 SQL"},
    {"word": "DML",                  "pron": "디엠엘",            "abbr": True,  "desc": "데이터 조작어",           "ex": "SELECT, INSERT, UPDATE, DELETE"},
    {"word": "DCL",                  "pron": "디씨엘",            "abbr": True,  "desc": "데이터 제어어",           "ex": "GRANT, REVOKE — 권한 관리 SQL"},
    {"word": "Domain",               "pron": "도메인",            "abbr": False, "desc": "도메인",                  "ex": "속성이 가질 수 있는 값의 범위 (예: 나이는 0~150)"},
    {"word": "Derived Attribute",    "pron": "디라이브드 어트리뷰트", "abbr": False, "desc": "파생 속성",           "ex": "다른 속성으로부터 계산되는 속성 (예: 나이 → 생년월일)"},
    {"word": "Entity",               "pron": "엔터티",            "abbr": False, "desc": "엔터티",                  "ex": "독립적으로 존재하는 사람, 사물, 개념의 집합"},
    {"word": "ERD",                  "pron": "이알디",            "abbr": True,  "desc": "개체-관계 다이어그램",    "ex": "Entity Relationship Diagram — 데이터 구조 시각화"},
    {"word": "Equi Join",            "pron": "이쿼 조인",         "abbr": False, "desc": "등가 조인",               "ex": "= 연산자를 사용하는 조인"},
    {"word": "Existence Dependency", "pron": "이그지스턴스 디펜던시", "abbr": False, "desc": "존재 종속",           "ex": "부모 엔터티가 없으면 자식 엔터티도 존재 불가"},
    {"word": "Foreign Key",          "pron": "포린 키",           "abbr": False, "desc": "외래키",                  "ex": "다른 테이블의 기본키를 참조하는 컬럼"},
    {"word": "Full Outer Join",      "pron": "풀 아우터 조인",    "abbr": False, "desc": "완전 외부 조인",          "ex": "양쪽 테이블의 모든 행을 반환"},
    {"word": "Functional Dependency","pron": "펑셔널 디펜던시",   "abbr": False, "desc": "함수적 종속",             "ex": "X → Y: X값이 결정되면 Y값도 결정됨"},
    {"word": "GROUP BY",             "pron": "그룹 바이",         "abbr": False, "desc": "그룹화",                  "ex": "특정 컬럼 기준으로 행을 묶어 집계"},
    {"word": "HAVING",               "pron": "해빙",              "abbr": False, "desc": "그룹 조건 필터",          "ex": "GROUP BY 이후 조건 적용 (WHERE는 그룹화 전)"},
    {"word": "Hierarchy",            "pron": "하이어라키",        "abbr": False, "desc": "계층 구조",               "ex": "상위-하위 관계로 구성된 데이터 구조"},
    {"word": "Index",                "pron": "인덱스",            "abbr": False, "desc": "인덱스",                  "ex": "검색 속도 향상을 위한 별도 자료구조"},
    {"word": "Instance",             "pron": "인스턴스",          "abbr": False, "desc": "인스턴스",                "ex": "엔터티의 실제 데이터 한 건 (= 행, 튜플)"},
    {"word": "Integrity",            "pron": "인테그리티",        "abbr": False, "desc": "무결성",                  "ex": "데이터가 정확하고 일관된 상태를 유지하는 성질"},
    {"word": "Inner Join",           "pron": "이너 조인",         "abbr": False, "desc": "내부 조인",               "ex": "두 테이블에서 조인 조건을 만족하는 행만 반환"},
    {"word": "Join",                 "pron": "조인",              "abbr": False, "desc": "조인",                    "ex": "두 개 이상의 테이블을 연결해 데이터를 조회"},
    {"word": "Key",                  "pron": "키",                "abbr": False, "desc": "키",                      "ex": "행을 고유하게 식별하는 컬럼 (PK, FK, UK 등)"},
    {"word": "Lookup Table",         "pron": "룩업 테이블",       "abbr": False, "desc": "참조 테이블",             "ex": "코드값의 의미를 저장하는 보조 테이블"},
    {"word": "Many-to-Many",         "pron": "매니 투 매니",      "abbr": False, "desc": "다대다 관계 (M:N)",       "ex": "학생-수업처럼 양쪽이 여러 개와 연결"},
    {"word": "Metadata",             "pron": "메타데이터",        "abbr": False, "desc": "메타데이터",              "ex": "데이터에 대한 데이터 (컬럼명, 타입, 길이 등)"},
    {"word": "Normalization",        "pron": "노멀라이제이션",    "abbr": False, "desc": "정규화",                  "ex": "중복을 제거하고 데이터 일관성을 높이는 과정"},
    {"word": "NULL",                 "pron": "널",                "abbr": False, "desc": "값 없음",                 "ex": "아직 알 수 없거나 해당 없는 값 (0이나 공백과 다름)"},
    {"word": "Non-key Attribute",    "pron": "논키 어트리뷰트",   "abbr": False, "desc": "비키 속성",               "ex": "기본키가 아닌 일반 속성"},
    {"word": "One-to-Many",          "pron": "원 투 매니",        "abbr": False, "desc": "일대다 관계 (1:N)",       "ex": "부서(1) — 직원(N) 관계"},
    {"word": "One-to-One",           "pron": "원 투 원",          "abbr": False, "desc": "일대일 관계 (1:1)",       "ex": "주민(1) — 여권(1) 관계"},
    {"word": "Outer Join",           "pron": "아우터 조인",       "abbr": False, "desc": "외부 조인",               "ex": "조인 조건 불만족 행도 포함해 반환"},
    {"word": "Primary Key",          "pron": "프라이머리 키",     "abbr": False, "desc": "기본키 (PK)",             "ex": "테이블에서 행을 유일하게 식별하는 컬럼"},
    {"word": "Projection",           "pron": "프로젝션",          "abbr": False, "desc": "프로젝션",                "ex": "필요한 컬럼만 선택해 조회 (SELECT절)"},
    {"word": "Partial Dependency",   "pron": "파셜 디펜던시",     "abbr": False, "desc": "부분 함수 종속",          "ex": "복합키 중 일부에만 종속 → 2NF 위반"},
    {"word": "Query",                "pron": "쿼리",              "abbr": False, "desc": "쿼리",                    "ex": "데이터를 조회하거나 조작하는 SQL 명령문"},
    {"word": "Relationship",         "pron": "릴레이션십",        "abbr": False, "desc": "관계",                    "ex": "두 엔터티 간의 연관성 (1:1, 1:N, M:N)"},
    {"word": "Redundancy",           "pron": "리던던시",          "abbr": False, "desc": "중복",                    "ex": "같은 데이터가 여러 곳에 저장돼 이상 현상 유발"},
    {"word": "Rollback",             "pron": "롤백",              "abbr": False, "desc": "롤백",                    "ex": "트랜잭션 이전 상태로 되돌리는 작업"},
    {"word": "Row",                  "pron": "로우",              "abbr": False, "desc": "행 / 튜플",               "ex": "테이블에서 가로 방향의 데이터 한 건"},
    {"word": "Schema",               "pron": "스키마",            "abbr": False, "desc": "스키마",                  "ex": "데이터베이스의 구조와 제약조건을 정의한 틀"},
    {"word": "Subquery",             "pron": "서브쿼리",          "abbr": False, "desc": "서브쿼리",                "ex": "쿼리 안에 포함된 또 다른 쿼리"},
    {"word": "Self Join",            "pron": "셀프 조인",         "abbr": False, "desc": "자기 참조 조인",          "ex": "같은 테이블을 두 번 조인 (조직도, 계층 구조)"},
    {"word": "Surrogate Key",        "pron": "서로게이트 키",     "abbr": False, "desc": "대리키",                  "ex": "의미 없는 인조키 (AUTO_INCREMENT 등)"},
    {"word": "Transaction",          "pron": "트랜잭션",          "abbr": False, "desc": "트랜잭션",                "ex": "하나의 논리적 작업 단위 (ACID 특성 보장)"},
    {"word": "Transitive Dependency","pron": "트랜지티브 디펜던시","abbr": False, "desc": "이행적 종속",            "ex": "A→B, B→C 이면 A→C — 3NF 위반"},
    {"word": "Table",                "pron": "테이블",            "abbr": False, "desc": "테이블",                  "ex": "관계형 DB에서 데이터를 저장하는 2차원 구조"},
    {"word": "Tuple",                "pron": "튜플",              "abbr": False, "desc": "튜플 / 행",               "ex": "테이블의 한 행 (= Row, Record)"},
    {"word": "Unique Key",           "pron": "유니크 키",         "abbr": False, "desc": "유일키",                  "ex": "NULL 허용하면서 중복 불가 제약조건"},
    {"word": "View",                 "pron": "뷰",                "abbr": False, "desc": "뷰",                      "ex": "저장된 SELECT 쿼리 — 가상 테이블"},
    {"word": "WHERE",                "pron": "웨어",              "abbr": False, "desc": "조건 필터",               "ex": "SELECT에서 행을 필터링하는 조건절"},
    {"word": "AVG",                  "pron": "에버리지",          "abbr": True,  "desc": "평균 집계 함수",          "ex": "AVG(salary) — 급여 평균 계산"},
    {"word": "COUNT",                "pron": "카운트",            "abbr": True,  "desc": "행 수 집계 함수",         "ex": "COUNT(*) — 전체 행 수 반환"},
    {"word": "SUM",                  "pron": "섬",                "abbr": True,  "desc": "합계 집계 함수",          "ex": "SUM(price) — 가격 합계 계산"},
    {"word": "MAX",                  "pron": "맥스",              "abbr": True,  "desc": "최댓값 집계 함수",        "ex": "MAX(score) — 최고 점수 반환"},
    {"word": "MIN",                  "pron": "민",                "abbr": True,  "desc": "최솟값 집계 함수",        "ex": "MIN(score) — 최저 점수 반환"},
]

def format_word_display(w):
    """카카오톡 표시용: 약어면 'CRUD크루드', 일반이면 'Attribute(어트리뷰트)'"""
    if w["abbr"]:
        return f"{w['word']}{w['pron']}"
    else:
        return f"{w['word']}({w['pron']})"

def pick_words():
    today = date.today()
    hour = __import__('datetime').datetime.now().hour
    if hour < 12:
        session = 0
    elif hour < 18:
        session = 1
    else:
        session = 2
    seed = int(today.strftime("%Y%m%d")) + session
    rng = random.Random(seed)
    return rng.sample(WORDS, 3)

def session_label():
    hour = __import__('datetime').datetime.now().hour
    if hour < 12:
        return "아침 세션"
    elif hour < 18:
        return "점심 세션"
    else:
        return "저녁 세션"

def build_message(words):
    today = date.today()
    month = today.month
    day   = today.day
    label = session_label()

    lines = [
        "🔤 SQLD 영어단어 퀴즈",
        f"📅 {month:02d}월 {day:02d}일 | {label}",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    for i, w in enumerate(words, 1):
        display = format_word_display(w)
        lines += [
            f"📌 단어 {i}: {display}",
            f"   🇰🇷 뜻: {w['desc']}",
            f"   💡 설명: {w['ex']}",
        ]
    lines += [
        "━━━━━━━━━━━━━━━━━━━━",
        "📚 더 많은 단어 퀴즈 풀기:",
        "https://pictory-droid.github.io/sqld-notion-study/english_quiz.html",
    ]
    return "\n".join(lines)

def send_kakao(text):
    res = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers={"Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}"},
        data={
            "template_object": json.dumps({
                "object_type": "text",
                "text": text,
                "link": {
                    "web_url": "https://pictory-droid.github.io/sqld-notion-study/english_quiz.html",
                    "mobile_web_url": "https://pictory-droid.github.io/sqld-notion-study/english_quiz.html",
                },
                "button_title": "퀴즈 풀기",
            })
        }
    )
    if res.status_code == 200:
        print("✅ 카카오톡 발송 성공")
    else:
        print(f"❌ 발송 실패: {res.status_code} {res.text}")

if __name__ == "__main__":
    words   = pick_words()
    message = build_message(words)
    print(message)
    send_kakao(message)
