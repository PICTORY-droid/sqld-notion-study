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

res = requests.get(
    f"https://api.notion.com/v1/blocks/{PARENT_PAGE_ID}/children",
    headers=HEADERS
)

print("\n📋 페이지 안의 DB 목록:")
for block in res.json().get("results", []):
    if block["type"] == "child_database":
        title = block["child_database"]["title"]
        db_id = block["id"]
        print(f"  {title} → {db_id}")