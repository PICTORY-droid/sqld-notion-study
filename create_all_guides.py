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

def create_page(emoji, title, children):
    url  = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        },
        "children": children
    }
    res = requests.post(url, headers=HEADERS, json=body)
    if res.status_code == 200:
        print(f"✅ {title} 생성 완료! → {res.json().get('url','')}")
    else:
        print(f"❌ 오류: {res.json().get('message','')}")

def callout(emoji, color, text):
    return {
        "object": "block", "type": "callout",
        "callout": {
            "rich_text": [{"text": {"content": text}}],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": color
        }
    }

def heading1(text):
    return {
        "object": "block", "type": "heading_1",
        "heading_1": {"rich_text": [{"text": {"content": text}}]}
    }

def heading2(text):
    return {
        "object": "block", "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": text}}]}
    }

divider = {"object": "block", "type": "divider", "divider": {}}

# =============================================
# 1. 이론 학습 DB 가이드
# =============================================
def create_theory_guide():
    children = [
        heading1("📖 이론 학습 DB 가이드"),
        callout("📖", "blue_background",
            "이론 학습 DB가 뭐예요?\n\n교재를 읽으면서 공부한 단원을 기록하는 공간이에요!\n어느 단원을 공부했는지, 얼마나 이해했는지 기록해두면\n나중에 복습할 때 정말 편해요 😊"
        ),
        callout("📌", "green_background",
            "작성 방법 — Git Bash 사용법\n\n① Git Bash 열기\n② 아래 명령어 복사해서 붙여넣기\n\npython add_theory.py \"단원명\" \"날짜\" \"과목\" \"이해도\"\n\n③ 과목은 아래 중 하나를 그대로 복사하세요!\n\"1과목 - 데이터 모델링\"  ← 1과목 공부했을 때\n\"2과목 - SQL 기본 및 활용\"  ← 2과목 공부했을 때\n\n④ 이해도는 아래 중 하나를 그대로 복사하세요!\n\"⭐ 잘 모름\"      ← 거의 모르겠을 때\n\"⭐⭐ 조금 앎\"    ← 조금은 알 것 같을 때\n\"⭐⭐⭐ 보통\"     ← 보통 정도 이해했을 때\n\"⭐⭐⭐⭐ 잘 앎\"  ← 잘 이해했을 때\n\"⭐⭐⭐⭐⭐ 완벽\" ← 완벽하게 이해했을 때\n\n💡 예시\npython add_theory.py \"엔터티와 속성\" \"2026-05-06\" \"1과목 - 데이터 모델링\" \"⭐⭐⭐ 보통\""
        ),
        callout("🔁", "yellow_background",
            "활용 팁\n\n공부 끝나고 노션에서 직접 체크하세요!\n복습필요 체크 ✅ → 복습 스케줄 DB에 추가하기\n완료 체크 ✅ → 이 단원 공부 완료!\n핵심키워드 → 이 단원에서 중요한 단어들 입력하기"
        ),
        divider,
        heading2("🎯 한눈에 보는 예시 3개"),
        callout("🎯", "gray_background",
            "예시 1) 1과목 공부한 경우\npython add_theory.py \"엔터티와 속성\" \"2026-05-06\" \"1과목 - 데이터 모델링\" \"⭐⭐⭐ 보통\"\n\n예시 2) 2과목 공부한 경우\npython add_theory.py \"SELECT 기본 문법\" \"2026-05-07\" \"2과목 - SQL 기본 및 활용\" \"⭐⭐ 조금 앎\"\n\n예시 3) 어려운 단원 공부한 경우\npython add_theory.py \"정규화 1~3단계\" \"2026-05-08\" \"1과목 - 데이터 모델링\" \"⭐ 잘 모름\""
        ),
    ]
    create_page("📖", "📖 이론 학습 가이드", children)

# =============================================
# 2. SQL 실습 DB 가이드
# =============================================
def create_sql_guide():
    children = [
        heading1("💻 SQL 실습 DB 가이드"),
        callout("💻", "blue_background",
            "SQL 실습 DB가 뭐예요?\n\nSQL 문법을 직접 써보면서 실습한 내용을 기록하는 공간이에요!\n어떤 문법을 실습했는지, 오류가 났는지 기록해두면\n나중에 헷갈릴 때 바로 찾아볼 수 있어요 😊"
        ),
        callout("📌", "green_background",
            "작성 방법 — Git Bash 사용법\n\n① Git Bash 열기\n② 아래 명령어 복사해서 붙여넣기\n\npython add_sql.py \"문법명\" \"날짜\" \"분류\" \"난이도\"\n\n③ 분류는 아래 중 하나를 그대로 복사하세요!\n\"SELECT (조회)\"     ← 데이터 조회할 때\n\"WHERE (조건)\"      ← 조건 걸 때\n\"JOIN (연결)\"       ← 테이블 합칠 때\n\"GROUP BY (그룹)\"   ← 그룹으로 묶을 때\n\"서브쿼리\"          ← 쿼리 안에 쿼리 쓸 때\n\"윈도우함수\"        ← 윈도우 함수 쓸 때\n\"DDL (테이블 생성)\" ← 테이블 만들 때\n\"DML (데이터 조작)\" ← 데이터 넣고 수정할 때\n\n④ 난이도는 아래 중 하나를 그대로 복사하세요!\n\"쉬움\"    ← 쉬웠을 때\n\"보통\"    ← 보통이었을 때\n\"어려움\"  ← 어려웠을 때\n\n💡 예시\npython add_sql.py \"GROUP BY 실습\" \"2026-05-06\" \"GROUP BY (그룹)\" \"보통\""
        ),
        callout("🔁", "yellow_background",
            "활용 팁\n\n오류가 났을 때 → 노션에서 오류발생 체크 ✅ + 오류원인 입력\n실습 완료하면 → 완료 체크 ✅\n\n같은 문법을 여러 번 실습해도 괜찮아요!\n날짜별로 기록되니까 내 성장을 볼 수 있어요 😊"
        ),
        divider,
        heading2("🎯 한눈에 보는 예시 3개"),
        callout("🎯", "gray_background",
            "예시 1) GROUP BY 실습\npython add_sql.py \"GROUP BY 실습\" \"2026-05-06\" \"GROUP BY (그룹)\" \"보통\"\n\n예시 2) JOIN 실습\npython add_sql.py \"INNER JOIN 실습\" \"2026-05-07\" \"JOIN (연결)\" \"어려움\"\n\n예시 3) SELECT 실습\npython add_sql.py \"SELECT 기본 조회\" \"2026-05-08\" \"SELECT (조회)\" \"쉬움\""
        ),
    ]
    create_page("💻", "💻 SQL 실습 가이드", children)

# =============================================
# 3. 문제풀이 DB 가이드
# =============================================
def create_quiz_guide():
    children = [
        heading1("❓ 문제풀이 DB 가이드"),
        callout("❓", "blue_background",
            "문제풀이 DB가 뭐예요?\n\n문제를 풀고 나서 결과를 기록하는 공간이에요!\n맞았는지 틀렸는지, 어디서 가져온 문제인지 기록해두면\n내가 어떤 문제를 잘 푸는지 파악할 수 있어요 😊"
        ),
        callout("📌", "green_background",
            "작성 방법 — Git Bash 사용법\n\n① Git Bash 열기\n② 아래 명령어 복사해서 붙여넣기\n\npython add_quiz.py \"문제명\" \"날짜\" \"출처\" \"과목\" \"정답여부\" \"난이도\"\n\n③ 출처는 아래 중 하나를 그대로 복사하세요!\n\"이기적 교재\"  ← 이기적 교재 문제\n\"기출문제\"     ← 실제 기출문제\n\"모의고사\"     ← 모의고사 문제\n\"인터넷 문제\"  ← 인터넷에서 찾은 문제\n\n④ 과목은 아래 중 하나를 그대로 복사하세요!\n\"1과목\"  ← 데이터 모델링 문제\n\"2과목\"  ← SQL 기본 및 활용 문제\n\n⑤ 정답여부는 아래 중 하나를 그대로 복사하세요!\n\"✅ 정답\"   ← 맞았을 때\n\"❌ 오답\"   ← 틀렸을 때\n\"🤔 찍음\"  ← 찍어서 맞았을 때\n\n⑥ 난이도는 아래 중 하나를 그대로 복사하세요!\n\"쉬움\" / \"보통\" / \"어려움\"\n\n💡 예시\npython add_quiz.py \"엔터티 식별자 문제\" \"2026-05-06\" \"이기적 교재\" \"1과목\" \"❌ 오답\" \"보통\""
        ),
        callout("🔁", "yellow_background",
            "활용 팁\n\n틀린 문제는 → 오답노트작성 체크 ✅ 후 오답 노트 DB에 추가!\n찍어서 맞은 문제도 → 오답 노트 DB에 추가하세요!\n정답률이 낮은 과목 → 더 집중해서 공부하기!"
        ),
        divider,
        heading2("🎯 한눈에 보는 예시 3개"),
        callout("🎯", "gray_background",
            "예시 1) 맞은 문제\npython add_quiz.py \"엔터티 식별자 문제\" \"2026-05-06\" \"이기적 교재\" \"1과목\" \"✅ 정답\" \"보통\"\n\n예시 2) 틀린 문제\npython add_quiz.py \"NULL 비교 문제\" \"2026-05-07\" \"기출문제\" \"2과목\" \"❌ 오답\" \"어려움\"\n\n예시 3) 찍은 문제\npython add_quiz.py \"GROUP BY 순서 문제\" \"2026-05-08\" \"모의고사\" \"2과목\" \"🤔 찍음\" \"보통\""
        ),
    ]
    create_page("❓", "❓ 문제풀이 가이드", children)

# =============================================
# 4. 복습 스케줄 DB 가이드
# =============================================
def create_review_guide():
    children = [
        heading1("🔁 복습 스케줄 DB 가이드"),
        callout("🔁", "blue_background",
            "복습 스케줄 DB가 뭐예요?\n\n공부한 내용을 까먹지 않도록 복습 날짜를 자동으로 잡아주는 공간이에요!\n사람은 배운 것을 금방 잊어버려요.\n1일 후 → 3일 후 → 7일 후 → 30일 후 복습하면 절대 안 잊어버려요 😊"
        ),
        callout("📌", "green_background",
            "작성 방법 — Git Bash 사용법\n\n① Git Bash 열기\n② 아래 명령어 복사해서 붙여넣기\n\npython add_review.py\n\n③ 그러면 이렇게 물어봐요!\n공부한 내용 입력 (예: 데이터 모델링 기본 개념):\n→ 오늘 공부한 내용을 입력하고 엔터!\n\n공부한 날짜 입력 (예: 2026-05-06):\n→ 오늘 날짜 입력하고 엔터!\n\n그러면 자동으로 복습 날짜 4개가 만들어져요!\n1일 후 복습일\n3일 후 복습일\n7일 후 복습일\n30일 후 복습일\n\n💡 예시\n공부한 내용: 엔터티와 속성 개념\n공부한 날짜: 2026-05-06"
        ),
        callout("🔁", "yellow_background",
            "활용 팁\n\n복습 날짜가 되면 → 노션에서 해당 항목 열기\n복습 완료하면 → 1차복습_완료 체크 ✅\n다음 복습 완료하면 → 2차복습_완료 체크 ✅\n...\n4차복습까지 완료하면 → 완벽하게 내 것이 된 거예요! 🎉\n\n복습하면서 메모할 것이 있으면 → 복습메모에 입력하세요!"
        ),
        divider,
        heading2("🎯 한눈에 보는 예시"),
        callout("🎯", "gray_background",
            "Git Bash에서 실행하면 이렇게 나와요!\n\n$ python add_review.py\n==================================================\n🔁 복습 스케줄 추가\n==================================================\n\n공부한 내용 입력 (예: 데이터 모델링 기본 개념): 엔터티와 속성 개념\n공부한 날짜 입력 (예: 2026-05-06): 2026-05-06\n\n✅ [2026-05-06] 엔터티와 속성 개념 복습 일정 추가 완료!\n   1차: 2026-05-07 / 2차: 2026-05-09 / 3차: 2026-05-13 / 4차: 2026-06-05"
        ),
    ]
    create_page("🔁", "🔁 복습 스케줄 가이드", children)


if __name__ == "__main__":
    print("=" * 50)
    print("📚 가이드 페이지 4개 생성 시작!")
    print("=" * 50)
    create_theory_guide()
    create_sql_guide()
    create_quiz_guide()
    create_review_guide()
    print("=" * 50)
    print("🎉 모든 가이드 페이지 생성 완료!")
    print("=" * 50)