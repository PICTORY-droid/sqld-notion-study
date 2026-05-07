import requests
import os
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

today = date.today()
stage1_end = date(2026, 6, 15)
stage2_end = date(2026, 7, 19)

if today <= stage1_end:
    stage = 1
    stage_label = "1단계 기초 다지기"
elif today <= stage2_end:
    stage = 2
    stage_label = "2단계 SQL 심화"
else:
    stage = 3
    stage_label = "3단계 최종 마무리"

questions = {
    1: [
        {"q": "엔터티(Entity)란 무엇인가?", "opts": ["데이터베이스 테이블", "독립적으로 존재하는 사람, 사물, 개념의 집합", "속성들의 묶음", "두 엔터티 간의 연결"], "ans": 2},
        {"q": "기본키(Primary Key)의 특징으로 올바른 것은?", "opts": ["NULL 허용", "중복 가능", "유일하고 NULL 불가", "여러 개 존재 가능"], "ans": 3},
        {"q": "NULL 비교 시 올바른 SQL은?", "opts": ["WHERE 컬럼 = NULL", "WHERE 컬럼 == NULL", "WHERE 컬럼 IS NULL", "WHERE 컬럼 = ''"], "ans": 3},
        {"q": "ORDER BY 기본 정렬 순서는?", "opts": ["내림차순(DESC)", "오름차순(ASC)", "삽입 순서", "랜덤"], "ans": 2},
        {"q": "SQL 실행 순서로 올바른 것은?", "opts": ["SELECT→FROM→WHERE→GROUP BY→HAVING→ORDER BY", "FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY", "FROM→SELECT→WHERE→GROUP BY→HAVING→ORDER BY", "SELECT→WHERE→FROM→GROUP BY→HAVING→ORDER BY"], "ans": 2},
        {"q": "데이터 모델링 3단계 순서로 올바른 것은?", "opts": ["물리→논리→개념", "개념→물리→논리", "개념→논리→물리", "논리→개념→물리"], "ans": 3},
        {"q": "TRUNCATE와 DELETE의 차이로 올바른 것은?", "opts": ["TRUNCATE는 롤백 가능", "DELETE는 DDL", "TRUNCATE는 DDL로 롤백 불가", "둘 다 동일"], "ans": 3},
        {"q": "COUNT(*)에 대한 설명으로 올바른 것은?", "opts": ["NULL 제외 행 수 반환", "NULL 포함 전체 행 수 반환", "고유값 수 반환", "합계 반환"], "ans": 2},
    ],
    2: [
        {"q": "INNER JOIN에 대한 설명으로 올바른 것은?", "opts": ["왼쪽 테이블 모든 행 반환", "조인 조건을 만족하는 행만 반환", "오른쪽 테이블 모든 행 반환", "모든 행 반환"], "ans": 2},
        {"q": "HAVING절에 대한 설명으로 올바른 것은?", "opts": ["그룹화 전 조건 필터링", "그룹화 후 조건 필터링", "WHERE절과 동일", "ORDER BY 뒤에 위치"], "ans": 2},
        {"q": "RANK()와 DENSE_RANK()의 차이로 올바른 것은?", "opts": ["차이 없음", "RANK()는 동순위 다음 건너뜀, DENSE_RANK()는 안 건너뜀", "DENSE_RANK()가 건너뜀", "RANK()는 NULL 무시"], "ans": 2},
        {"q": "제2정규형(2NF)이 되기 위한 조건은?", "opts": ["원자값을 가져야 한다", "부분 함수 종속을 제거", "이행 함수 종속을 제거", "다치 종속을 제거"], "ans": 2},
        {"q": "UNION과 UNION ALL의 차이로 올바른 것은?", "opts": ["UNION이 중복 포함", "UNION이 중복 제거, UNION ALL은 중복 포함", "둘 다 동일", "UNION ALL만 사용 가능"], "ans": 2},
        {"q": "윈도우 함수에 대한 설명으로 올바른 것은?", "opts": ["GROUP BY와 동일", "행 간 관계 정의, 결과 행 수 유지", "WHERE절에서만 사용", "반드시 PARTITION BY 필요"], "ans": 2},
    ],
    3: [
        {"q": "RANK() 결과: (홍길동,90), (김철수,90), (이영희,85) 순위는?", "opts": ["1,2,3", "1,1,2", "1,1,3", "0,0,1"], "ans": 3},
        {"q": "NOT IN에 NULL 포함 시 결과는?\nWHERE 학년 NOT IN (1,2,NULL)", "opts": ["학년이 1,2 아닌 모든 행", "빈 결과셋", "학년 NULL인 행", "모든 행"], "ans": 2},
        {"q": "인덱스가 사용되지 않는 경우는?", "opts": ["WHERE 컬럼 = 100", "WHERE 컬럼 BETWEEN 1 AND 100", "WHERE 컬럼 LIKE '홍%'", "WHERE SUBSTR(컬럼,1,2) = '홍길'"], "ans": 4},
        {"q": "SUM 함수에서 조건에 맞는 행이 없을 때 결과는?", "opts": ["0", "NULL", "오류", "빈 결과셋"], "ans": 2},
    ]
}

qs = questions[stage]
selected = random.sample(qs, min(2, len(qs)))

num_map = ["①", "②", "③", "④"]

def format_question(q, idx):
    opts_text = "\n".join([f"  {num_map[i]} {o}" for i, o in enumerate(q["opts"])])
    answer = f"{num_map[q['ans']-1]} {q['opts'][q['ans']-1]}"
    return f"""📌 문제 {idx}
{q['q']}

{opts_text}

✅ 정답: {answer}"""

msg_lines = [
    f"📚 [{stage_label}] SQLD 퀴즈",
    f"📅 {today.strftime('%m월 %d일')} | 오늘도 화이팅!",
    "━" * 20,
]
for i, q in enumerate(selected, 1):
    msg_lines.append(format_question(q, i))
    msg_lines.append("")

msg_lines.append("━" * 20)
msg_lines.append("🔗 더 많은 문제: https://pictory-droid.github.io/sqld-notion-study/quiz.html")

message = "\n".join(msg_lines)

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
headers = {
    "Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded",
}
template = {
    "object_type": "text",
    "text": message,
    "link": {
        "web_url": "https://pictory-droid.github.io/sqld-notion-study/quiz.html",
        "mobile_web_url": "https://pictory-droid.github.io/sqld-notion-study/quiz.html"
    }
}
import json
data = {"template_object": json.dumps(template)}
res = requests.post(url, headers=headers, data=data)

if res.status_code == 200:
    print("✅ 카카오톡 퀴즈 전송 완료!")
    print(f"   단계: {stage_label}")
    print(f"   문제 수: {len(selected)}개")
else:
    print(f"❌ 오류: {res.json()}")