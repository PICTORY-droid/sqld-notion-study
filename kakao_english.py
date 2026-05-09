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
WORDS = [
    {"word": "Attribute", "desc": "속성", "ex": "엔터티가 가지는 세부 데이터 항목 (예: 이름, 나이)"},
    {"word": "Aggregate Function", "desc": "집계 함수", "ex": "여러 행을 하나의 결과로 반환 (SUM, AVG, COUNT 등)"},
    {"word": "Association", "desc": "연관 / 관계", "ex": "두 엔터티 간의 관계를 나타냄"},
    {"word": "Business Rule", "desc": "업무 규칙", "ex": "데이터 모델링의 기반이 되는 업무 요건"},
    {"word": "Cardinality", "desc": "카디널리티 / 집합의 원소 수", "ex": "1:1, 1:N, M:N 관계를 나타냄"},
    {"word": "Column", "desc": "열 / 컬럼", "ex": "테이블에서 세로 방향의 데이터 항목"},
    {"word": "Constraint", "desc": "제약조건", "ex": "PK, FK, UNIQUE, NOT NULL 등 데이터 무결성 규칙"},
    {"word": "CRUD", "desc": "생성·조회·수정·삭제", "ex": "Create, Read, Update, Delete의 약자"},
    {"word": "Composite Key", "desc": "복합키", "ex": "두 개 이상의 컬럼으로 이루어진 기본키"},
    {"word": "Cascading", "desc": "연쇄 처리", "ex": "부모 행 삭제 시 자식 행도 함께 삭제되는 옵션"},
    {"word": "Data Model", "desc": "데이터 모델", "ex": "현실 세계 데이터를 추상화해 표현한 구조"},
    {"word": "DDL", "desc": "데이터 정의어", "ex": "CREATE, ALTER, DROP 등 구조를 정의하는 SQL"},
    {"word": "DML", "desc": "데이터 조작어", "ex": "SELECT, INSERT, UPDATE, DELETE"},
    {"word": "DCL", "desc": "데이터 제어어", "ex": "GRANT, REVOKE — 권한 관리 SQL"},
    {"word": "Domain", "desc": "도메인", "ex": "속성이 가질 수 있는 값의 범위 (예: 나이는 0~150)"},
    {"word": "Derived Attribute", "desc": "파생 속성", "ex": "다른 속성으로부터 계산되는 속성 (예: 나이 → 생년월일)"},
    {"word": "Entity", "desc": "엔터티", "ex": "독립적으로 존재하는 사람, 사물, 개념의 집합"},
    {"word": "ERD", "desc": "개체-관계 다이어그램", "ex": "Entity Relationship Diagram — 데이터 구조 시각화"},
    {"word": "Equi Join", "desc": "등가 조인", "ex": "= 연산자를 사용하는 조인"},
    {"word": "Existence Dependency", "desc": "존재 종속", "ex": "부모 엔터티가 없으면 자식 엔터티도 존재 불가"},
    {"word": "Foreign Key", "desc": "외래키", "ex": "다른 테이블의 기본키를 참조하는 컬럼"},
    {"word": "Full Outer Join", "desc": "완전 외부 조인", "ex": "양쪽 테이블의 모든 행을 반환"},
    {"word": "Functional Dependency", "desc": "함수적 종속", "ex": "X → Y: X값이 결정되면 Y값도 결정됨"},
    {"word": "GROUP BY", "desc": "그룹화", "ex": "특정 컬럼 기준으로 행을 묶어 집계"},
    {"word": "HAVING", "desc": "그룹 조건 필터", "ex": "GROUP BY 이후 조건 적용 (WHERE는 그룹화 전)"},
    {"word": "Hierarchy", "desc": "계층 구조", "ex": "상위-하위 관계로 구성된 데이터 구조"},
    {"word": "Index", "desc": "인덱스", "ex": "검색 속도 향상을 위한 별도 자료구조"},
    {"word": "Instance", "desc": "인스턴스", "ex": "엔터티의 실제 데이터 한 건 (= 행, 튜플)"},
    {"word": "Integrity", "desc": "무결성", "ex": "데이터가 정확하고 일관된 상태를 유지하는 성질"},
    {"word": "Inner Join", "desc": "내부 조인", "ex": "두 테이블에서 조인 조건을 만족하는 행만 반환"},
    {"word": "Join", "desc": "조인", "ex": "두 개 이상의 테이블을 연결해 데이터를 조회"},
    {"word": "Key", "desc": "키", "ex": "행을 고유하게 식별하는 컬럼 (PK, FK, UK 등)"},
    {"word": "Lookup Table", "desc": "참조 테이블", "ex": "코드값의 의미를 저장하는 보조 테이블"},
    {"word": "Many-to-Many", "desc": "다대다 관계 (M:N)", "ex": "학생-수업처럼 양쪽이 여러 개와 연결"},
    {"word": "Metadata", "desc": "메타데이터", "ex": "데이터에 대한 데이터 (컬럼명, 타입, 길이 등)"},
    {"word": "Normalization", "desc": "정규화", "ex": "중복을 제거하고 데이터 일관성을 높이는 과정"},
    {"word": "NULL", "desc": "널 / 값 없음", "ex": "아직 알 수 없거나 해당 없는 값 (0이나 공백과 다름)"},
    {"word": "Non-key Attribute", "desc": "비키 속성", "ex": "기본키가 아닌 일반 속성"},
    {"word": "One-to-Many", "desc": "일대다 관계 (1:N)", "ex": "부서(1) — 직원(N) 관계"},
    {"word": "One-to-One", "desc": "일대일 관계 (1:1)", "ex": "주민(1) — 여권(1) 관계"},
    {"word": "Outer Join", "desc": "외부 조인", "ex": "조인 조건 불만족 행도 포함해 반환"},
    {"word": "Primary Key", "desc": "기본키 (PK)", "ex": "테이블에서 행을 유일하게 식별하는 컬럼"},
    {"word": "Projection", "desc": "프로젝션", "ex": "필요한 컬럼만 선택해 조회 (SELECT절)"},
    {"word": "Partial Dependency", "desc": "부분 함수 종속", "ex": "복합키 중 일부에만 종속 → 2NF 위반"},
    {"word": "Query", "desc": "쿼리", "ex": "데이터를 조회하거나 조작하는 SQL 명령문"},
    {"word": "Relationship", "desc": "관계", "ex": "두 엔터티 간의 연관성 (1:1, 1:N, M:N)"},
    {"word": "Redundancy", "desc": "중복", "ex": "같은 데이터가 여러 곳에 저장돼 이상 현상 유발"},
    {"word": "Rollback", "desc": "롤백", "ex": "트랜잭션 이전 상태로 되돌리는 작업"},
    {"word": "Row", "desc": "행 / 튜플", "ex": "테이블에서 가로 방향의 데이터 한 건"},
    {"word": "Schema", "desc": "스키마", "ex": "데이터베이스의 전체 구조 정의"},
    {"word": "Subquery", "desc": "서브쿼리", "ex": "쿼리 안에 포함된 또 다른 쿼리"},
    {"word": "Self Join", "desc": "셀프 조인", "ex": "같은 테이블을 두 번 조인 (계층 구조 조회 등)"},
    {"word": "Table", "desc": "테이블", "ex": "행과 열로 구성된 관계형 데이터 저장 구조"},
    {"word": "Transaction", "desc": "트랜잭션", "ex": "ACID를 보장하는 논리적 작업 단위"},
    {"word": "Tuple", "desc": "튜플 / 행", "ex": "테이블에서 하나의 데이터 레코드"},
    {"word": "Transitive Dependency", "desc": "이행 함수 종속", "ex": "A→B→C: A가 C를 간접 결정 → 3NF 위반"},
    {"word": "UNION", "desc": "합집합 (중복 제거)", "ex": "두 쿼리 결과를 합치고 중복 제거"},
    {"word": "UNION ALL", "desc": "합집합 (중복 포함)", "ex": "두 쿼리 결과를 합치고 중복 유지"},
    {"word": "Unique Key", "desc": "유일키 (UK)", "ex": "NULL은 허용하지만 중복 불가한 키"},
    {"word": "Update Anomaly", "desc": "갱신 이상", "ex": "중복 데이터 일부만 수정 시 불일치 발생"},
    {"word": "View", "desc": "뷰", "ex": "SELECT 결과를 저장한 가상 테이블"},
    {"word": "WHERE", "desc": "조건절", "ex": "행을 필터링하는 SQL 조건 (그룹화 전 적용)"},
    {"word": "Workload", "desc": "작업 부하", "ex": "시스템이 처리하는 데이터 요청의 양"},
]

# 날짜 + 시간대 기반 시드 → 하루 3회 다른 단어 발송
today = date.today()
import datetime
hour = datetime.datetime.now().hour
if hour < 10:
    slot = 0
elif hour < 16:
    slot = 1
else:
    slot = 2

seed = int(today.strftime("%Y%m%d")) * 10 + slot
random.seed(seed)
selected = random.sample(WORDS, 3)

# 메시지 구성
slot_label = "아침" if slot == 0 else "점심" if slot == 1 else "저녁"
lines = [
    f"🔤 SQLD 영어단어 퀴즈",
    f"📅 {today.strftime('%m월 %d일')} | {slot_label} 세션",
    "━" * 20,
]

for i, w in enumerate(selected, 1):
    lines.append(f"📌 단어 {i}: {w['word']}")
    lines.append(f"   🇰🇷 뜻: {w['desc']}")
    lines.append(f"   💡 설명: {w['ex']}")
    lines.append("")

lines.append("━" * 20)
lines.append("📚 더 많은 단어 퀴즈 풀기:")
lines.append("https://pictory-droid.github.io/sqld-notion-study/english_quiz.html")

message = "\n".join(lines)

# 카카오톡 발송
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
headers = {
    "Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded",
}
template = {
    "object_type": "text",
    "text": message,
    "link": {
        "web_url": "https://pictory-droid.github.io/sqld-notion-study/english_quiz.html",
        "mobile_web_url": "https://pictory-droid.github.io/sqld-notion-study/english_quiz.html"
    }
}
data = {"template_object": json.dumps(template)}
res = requests.post(url, headers=headers, data=data)

if res.status_code == 200:
    print("✅ 카카오톡 영어단어 전송 완료!")
    print(f"   세션: {slot_label} ({slot+1}/3)")
    print(f"   단어: {', '.join([w['word'] for w in selected])}")
else:
    print(f"❌ 오류: {res.json()}")
