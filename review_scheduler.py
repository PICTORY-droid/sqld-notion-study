from datetime import date, timedelta

def calculate_review_dates(study_date):
    print(f"\n📅 학습일: {study_date.strftime('%Y년 %m월 %d일')}")
    print("-" * 35)
    for days, label in [(1, "1차"), (3, "2차"), (7, "3차"), (30, "4차")]:
        review = study_date + timedelta(days=days)
        print(f"  {label} 복습 (+{days:2d}일) → {review.strftime('%Y년 %m월 %d일')}")

if __name__ == "__main__":
    print("=" * 40)
    print("🔁 에빙하우스 망각곡선 복습 계산기")
    print("=" * 40)
    date_str = input("\n공부한 날짜를 입력하세요 (예: 20260506): ").strip()
    try:
        y = int(date_str[:4])
        m = int(date_str[4:6])
        d = int(date_str[6:8])
        calculate_review_dates(date(y, m, d))
        print("\n💡 노션 복습 스케줄 DB에 위 날짜를 입력하세요!")
    except:
        print("❌ 날짜 형식이 맞지 않아요. 예시: 20260506")