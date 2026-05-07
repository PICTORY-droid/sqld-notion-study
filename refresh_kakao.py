import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
KAKAO_REST_API_KEY  = os.getenv("KAKAO_REST_API_KEY")
KAKAO_REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN")

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
    new_access = data["access_token"]
    print(f"✅ 새 액세스 토큰:\n{new_access}")

    # .env 자동 업데이트
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r"KAKAO_ACCESS_TOKEN=.*", f"KAKAO_ACCESS_TOKEN={new_access}", content)

    if "refresh_token" in data:
        new_refresh = data["refresh_token"]
        content = re.sub(r"KAKAO_REFRESH_TOKEN=.*", f"KAKAO_REFRESH_TOKEN={new_refresh}", content)
        print(f"✅ 리프레시 토큰도 갱신됨:\n{new_refresh}")

    with open(".env", "w", encoding="utf-8") as f:
        f.write(content)

    print("\n✅ .env 업데이트 완료!")
    print("\n⚠️  GitHub Secrets에서 KAKAO_ACCESS_TOKEN 값도 위 토큰으로 교체하세요!")
else:
    print(f"❌ 실패: {data}")