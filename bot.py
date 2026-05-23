import os
import json
import asyncio
import discord

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright

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

playwright = None
browser = None


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
    global browser

    page = await browser.new_page()

    await page.goto(URL, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(1500)

    html = await page.content()
    await page.close()

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tr")

    print(f"읽은 게시글 row 수: {len(rows)}")

    posts = []

    for row in rows:
        tds = row.select("td")

        if len(tds) < 5:
            continue

        # 카테고리: 자유 / 추첨 등
        category_el = row.select_one("td:first-child span.rounded-full")
        category = category_el.get_text(" ", strip=True) if category_el else ""

        title_el = row.select_one("span.truncate.hover\\:underline")
        if not title_el:
            continue

        title = title_el.get_text(" ", strip=True)
        if not title:
            continue

        # 제외 키워드가 들어간 제목은 알림 제외
        if any(exclude in title for exclude in EXCLUDE_KEYWORDS):
            print("제외된 글:", title)
            continue

        is_keyword_matched = any(keyword in title for keyword in KEYWORDS)
        is_raffle_category = category == "추첨"

        # 제목에 감지 키워드가 있거나, 카테고리가 추첨이면 알림 대상
        if not is_keyword_matched and not is_raffle_category:
            continue

        time_text = tds[-1].get_text(" ", strip=True)

        if not is_recent(time_text):
            continue

        author = tds[3].get_text(" ", strip=True)
        author = author.replace("Level image", "").strip()

        # 게시글 ID 추출: popovertarget="138337"
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
    global playwright, browser

    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("채널을 찾을 수 없습니다.")
        return

    print("playwright 시작 전")

    playwright = await async_playwright().start()

    print("playwright 시작 완료")

    browser = await playwright.chromium.launch(
        executable_path="/usr/bin/chromium-browser",
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )

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