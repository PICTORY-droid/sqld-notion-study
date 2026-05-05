# 📚 SQLD 노션 학습 시스템

비전공자를 위한 SQLD 자격증 공부 노션 자동화 프로젝트

## 📅 학습 일정
- 공부 시작: 2026년 5월 6일
- 시험 접수: 2026년 7월 20일 ~ 24일
- 시험일: 2026년 8월 22일 (D-108)

## 🗂️ 만들어지는 노션 DB
1. 📖 이론 학습 DB
2. 💻 SQL 실습 DB
3. 🔁 복습 스케줄 DB (에빙하우스 망각곡선 기반)
4. ❓ 문제풀이 DB
5. 📝 오답 노트 DB
6. 📅 학습 계획 DB

## 🚀 사용 방법

### 1. 라이브러리 설치
pip install -r requirements.txt

### 2. .env 파일에 API 키 입력
NOTION_TOKEN=secret_xxxxx
PARENT_PAGE_ID=xxxxxxxx

### 3. 노션 DB 자동 생성
python setup_notion.py

### 4. 복습 알람 날짜 계산
python review_scheduler.py