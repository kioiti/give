import os
import json
import random
import discord
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

DATA_FILE = "activity.json"

# ---------------- 데이터 로드 ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------- 밈 데이터 ----------------
luck = [
    "오늘 운: SSS급 🔥",
    "오늘 운: 망함 😭",
    "오늘 운: 평범",
    "오늘 운: 떡상 각이다 📈",
    "오늘 운: 접속하지 마라"
]

whine = [
    "아니 왜 또 지냐?",
    "이건 게임이 문제가 있다",
    "팀원이 문제다",
    "내 손이 문제다 (아님)",
    "오늘은 운이 없다"
]

daily = [
    "오늘은 꼭 한 판 이겨보자",
    "연패하면 쉬어라",
    "오늘은 각 잡히는 날이다",
    "운빨 믿지 말고 실력으로 가자"
]


# ---------------- 메시지 기록 ----------------
user_count = defaultdict(int)


@client.event
async def on_ready():
    print(f"{client.user} 로그인 완료")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user = str(message.author.id)

    # ---------------- 통계 기록 ----------------
    data = load_data()
    data[user] = data.get(user, 0) + 1
    save_data(data)

    content = message.content.strip()

    # ---------------- 밈 기능 ----------------
    if content == "!운빨":
        await message.channel.send(random.choice(luck))
        return

    if content == "!징징":
        await message.channel.send(random.choice(whine))
        return

    if content == "!오늘":
        await message.channel.send(random.choice(daily))
        return

    # ---------------- 내 순위 ----------------
    if content == "!내순위":
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for i, (uid, count) in enumerate(sorted_data, 1):
            if uid == user:
                await message.channel.send(f"당신은 서버 {i}등입니다 (메시지 {count}개)")
                return

    # ---------------- 전체 랭킹 ----------------
    if content == "!랭킹":
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        msg = "📊 서버 활동 랭킹\n"
        for i, (uid, count) in enumerate(sorted_data[:5], 1):
            member = await client.fetch_user(int(uid))
            msg += f"{i}. {member.name} - {count}개\n"

        await message.channel.send(msg)


client.run(TOKEN)