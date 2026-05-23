import os
import json
import asyncio
import discord
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

CHECK_INTERVAL = 60

URL = "https://tr.game.onstove.com/community/runners/all?page=1"
BASE_DETAIL_URL = "https://tr.game.onstove.com/community/runners/all"

KEYWORDS = ["나눔", "추첨", "선착순"]
EXCLUDE_KEYWORDS = ["글증", "후기"]

SEEN_FILE = "seen_posts.json"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://tr.game.onstove.com/",
}


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen)[-500:], f, ensure_ascii=False, indent=2)


def is_recent(time_text: str):
    time_text = time_text.strip()

    if "방금" in time_text:
        return True

    if "분 전" in time_text:
        return True

    if "시간 전" in time_text:
        try:
            hour = int(time_text.replace("시간 전", "").strip())
            return hour <= 1
        except:
            return False

    return False


async def fetch_posts():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    options = Options()

    options.binary_location = "/usr/bin/chromium-browser"

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(URL)

    await asyncio.sleep(3)

    html = driver.page_source

    print(html[:3000])
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    rows = soup.select("tr.border-b")

    print(f"읽은 게시글 row 수: {len(rows)}")

    posts = []

    for row in rows:
        tds = row.select("td")

        if len(tds) < 5:
            continue

        category_el = row.select_one("td:first-child span.rounded-full")
        category = category_el.get_text(" ", strip=True) if category_el else ""

        title_el = row.select_one("span.truncate.hover\\:underline")

        if not title_el:
            continue

        title = title_el.get_text(" ", strip=True)

        if not title:
            continue

        if any(exclude in title for exclude in EXCLUDE_KEYWORDS):
            continue

        is_keyword_matched = any(keyword in title for keyword in KEYWORDS)
        is_raffle_category = category == "추첨"

        if not is_keyword_matched and not is_raffle_category:
            continue

        time_text = tds[-1].get_text(" ", strip=True)

        if not is_recent(time_text):
            continue

        author = tds[3].get_text(" ", strip=True)
        author = author.replace("Level image", "").strip()

        post_id = None

        button_el = row.select_one("button[popovertarget]")

        if button_el:
            post_id = button_el.get("popovertarget")

        if post_id:
            link = f"{BASE_DETAIL_URL}/{post_id}?page=1"
            post_key = post_id
        else:
            link = URL
            post_key = f"{title}|{author}"

        matched_keywords = [
            keyword for keyword in KEYWORDS
            if keyword in title
        ]

        if is_raffle_category and "추첨" not in matched_keywords:
            matched_keywords.append("추첨카테고리")

        posts.append({
            "key": post_key,
            "title": title,
            "author": author,
            "time": time_text,
            "link": link,
            "matched_keywords": matched_keywords,
            "category": category,
        })

    print(f"감지된 키워드 게시글 수: {len(posts)}")

    return posts


async def monitor():
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("채널을 찾을 수 없습니다.")
        return

    seen = load_seen()

    print("모니터링 시작")

    while not client.is_closed():
        try:
            posts = await fetch_posts()

            for post in posts:
                if post["key"] in seen:
                    continue

                seen.add(post["key"])
                save_seen(seen)

                message = (
                    f"🚨 런너게시판 "
                    f"[{', '.join(post['matched_keywords'])}] "
                    f"게시글 발견!\n\n"
                    f"🏷️ 분류: {post['category']}\n"
                    f"📝 제목: {post['title']}\n"
                    f"👤 작성자: {post['author']}\n"
                    f"⏰ 작성시간: {post['time']}\n"
                    f"🔗 링크:\n{post['link']}"
                )

                await channel.send(message)

                print("알림 전송:", post["title"])

        except Exception as e:
            print("오류 발생:", e)

        await asyncio.sleep(CHECK_INTERVAL)


@client.event
async def on_ready():
    print(f"{client.user} 로그인 완료")
    client.loop.create_task(monitor())


client.run(DISCORD_TOKEN)