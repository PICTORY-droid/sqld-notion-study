import requests
import os
from dotenv import load_dotenv

load_dotenv()

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
REDIRECT_URI = "https://pictory-droid.github.io"

def get_auth_url():
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&scope=talk_message"
    print("\n" + "=" * 50)
    print("📱 카카오 로그인 URL")
    print("=" * 50)
    print(f"\n아래 URL을 브라우저에 붙여넣고 로그인하세요!\n")
    print(url)
    print("\n로그인 후 리다이렉트된 URL에서")
    print("'code=' 뒤의 값을 복사해서 입력하세요!")
    print("=" * 50)

def get_token(code):
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    res = requests.post(url, data=data)
    if res.status_code == 200:
        token = res.json()
        print("\n✅ 토큰 발급 완료!")
        print(f"\n아래 내용을 .env 파일에 추가하세요!")
        print("=" * 50)
        print(f"KAKAO_ACCESS_TOKEN={token['access_token']}")
        print(f"KAKAO_REFRESH_TOKEN={token['refresh_token']}")
        print("=" * 50)
    else:
        print(f"❌ 오류: {res.json()}")

if __name__ == "__main__":
    get_auth_url()
    code = input("\ncode 값 입력: ").strip()
    get_token(code)