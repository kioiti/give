# =========================================================
# 디스코드 낚시 + 카지노 + 강화 RPG 봇
# =========================================================

import os
import json
import random
import datetime
import asyncio
import discord

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# =========================================================
# 파일
# =========================================================

DATA_FILE = "activity.json"
MONEY_FILE = "money.json"
ROD_FILE = "rod.json"
CHECKIN_FILE = "checkin.json"
PROTECT_FILE = "protect.json"

FISH_FILE = "fish_inventory.json"
FISH_COUNT_FILE = "fish_count.json"
AUTO_FILE = "auto_fishing.json"
SKIN_FILE = "skin.json"
BOSS_FILE = "boss.json"

# =========================================================
# 유저 매핑
# =========================================================

USER_MAP = {
    1501525905833594900: "머래",
    261016503963353098: "계삭",
    464655989996519424: "마라콩",
    707895110972473345: "밈콩",
    435351384137662464: "지성콩",
    1004779456696688760: "미희여사",
    706114030061879296: "에빙",
}

# =========================================================
# 운빨
# =========================================================

luck = [
    "오늘 운: SSS급 🔥",
    "오늘 운: 전설급 💸",
    "오늘 운: 멘탈 흔들림 🫠",
    "오늘 운: 판단력 상승 📈",
    "오늘 운: 억까 ON 💀",
    "오늘 운: 서버가 밀어줌 ⚡",
    "오늘 운: 도파민 MAX 🚨",
    "오늘 운: 강화각 떴다 🔨",
    "오늘 운: 지갑 조심 💳",
    "오늘 운: 채팅만 쳐도 웃김 😂",
    "오늘 운: 갑자기 폼 미침 🔥",
    "오늘 운: 버그급 행운 👑",
    "오늘 운: 물욕센서 감지됨 🎣",
    "오늘 운: 개같이 멸망 예정 ☠️",
    "오늘 운: 숨만 쉬어도 이득 😎",
    "오늘 운: 집중력 500% 📚",
    "오늘 운: 오늘만큼은 주인공 🌈",
    "오늘 운: 현타 조심 🫠",
    "오늘 운: 이상하게 다 잘됨 🤨",
    "오늘 운: 되는 날이다 ㄹㅇ",
    "오늘 운: 그냥 GOAT 🐐",
    "오늘 운: 억텐 금지 🚫",
    "오늘 운: 강화 누르면 터짐 💣",
    "오늘 운: 누가 봐도 레전드 📈",
    "오늘 운: 인생 치트키 활성화 ✨",
    "오늘 운: 카리나급 비주얼 😳",
    "오늘 운: 알빠노 모드 😌",
    "오늘 운: 폼 돌아옴 🔥",
    "오늘 운: 개큰행복 예정 🎉",
    "오늘 운: 뇌 빼고 하면 성공 🤯",
]

daily = [
    "오늘은 집중각 🎯",
    "오늘은 흐름 타기 🌊",
    "오늘은 천천히 가자 🚶",
    "오늘은 강화 금지 💀",
    "오늘은 도박 잘됨 🎰",
    "오늘은 물욕센서 OFF 🎣",
    "오늘은 그냥 눌러 🔥",
    "오늘은 억까 대비 🛡",
    "오늘은 기강 잡는 날 😎",
    "오늘은 무지성 플레이 ⚡",
    "오늘은 일단 드가자 🚀",
    "오늘은 숨참고 강화 ㄱㄱ",
    "오늘은 멘탈 관리 필수 🫠",
    "오늘은 GOAT 모드 🐐",
    "오늘은 채팅만 쳐도 웃김 😂",
    "오늘은 폼 미쳤다 📈",
    "오늘은 운빨캐 확정 🍀",
    "오늘은 현생 버프 ON ☀️",
    "오늘은 개같이 부활 🔥",
    "오늘은 손 떨리면 멈춰 ✋",
    "오늘은 진짜 되는 날 👑",
    "오늘은 서버가 밀어준다 ⚡",
    "오늘은 가챠각 🎲",
    "오늘은 레전드 찍는다 🌈",
    "오늘은 뇌 빼고 즐기기 🤪",
]


# =========================================================
# JSON
# =========================================================

def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =========================================================
# 강화
# =========================================================

MAX_LEVEL = 15


def get_upgrade_cost(level):
    return 500 + (level * 500)


def get_success_rate(level):

    rates = {
        0: 95,
        1: 90,
        2: 85,
        3: 80,
        4: 75,
        5: 65,
        6: 55,
        7: 45,
        8: 35,
        9: 30,
        10: 25,
        11: 20,
        12: 15,
        13: 10,
        14: 5
    }

    return rates.get(level, 3)


def get_rod_name(level):

    if level <= 3:
        return "🐟 초보 낚시대"

    elif level <= 6:
        return "🎣 일반 낚시대"

    elif level <= 9:
        return "✨ 강화 낚시대"

    elif level <= 11:
        return "🔥 희귀 낚시대"

    elif level <= 14:
        return "🌈 전설 낚시대"

    else:
        return "👑 테런 낚시대"

# =========================================================
# 물고기
# =========================================================

FISHES = [
    {"name": "🐟 잉어", "price": 300, "chance": 40},
    {"name": "🐠 고등어", "price": 500, "chance": 30},
    {"name": "🦈 상어", "price": 3000, "chance": 10},
    {"name": "🐡 복어", "price": 1500, "chance": 15},
    {"name": "🐉 용왕어", "price": 10000, "chance": 4},
    {"name": "👑 황금잉어", "price": 30000, "chance": 1},
]

BOSS_FISH = [
    "🔥 불멸의 상어",
    "🌊 심해 크라켄",
    "⚡ 천둥 메기",
    "👑 바다의 황제",
]

SKINS = {
    "기본": 0,
    "불꽃": 50000,
    "얼음": 70000,
    "전설": 150000
}

# =========================================================
# 랜덤 물고기
# =========================================================

def roll_fish(rod_level):

    bonus = rod_level * 0.5

    total = 0

    for fish in FISHES:
        total += fish["chance"] + bonus

    rand = random.uniform(0, total)

    current = 0

    for fish in FISHES:

        current += fish["chance"] + bonus

        if rand <= current:
            return fish

    return FISHES[0]

# =========================================================
# 시작
# =========================================================

@client.event
async def on_ready():

    print(f"{client.user} 로그인 완료")


# =========================================================
# 자동 낚시
# =========================================================

async def auto_fishing_loop():

    await client.wait_until_ready()

    while not client.is_closed():

        auto = load_json(AUTO_FILE)
        rods = load_json(ROD_FILE)
        inventory = load_json(FISH_FILE)
        fish_count = load_json(FISH_COUNT_FILE)

        for uid in auto:

            if not auto[uid]:
                continue

            rod_level = rods.get(uid, 0)

            fish = roll_fish(rod_level)

            if uid not in inventory:
                inventory[uid] = {}

            inventory[uid][fish["name"]] = (
                inventory[uid].get(fish["name"], 0) + 1
            )

            fish_count[uid] = fish_count.get(uid, 0) + 1

        save_json(FISH_FILE, inventory)
        save_json(FISH_COUNT_FILE, fish_count)

        await asyncio.sleep(300)

# =========================================================
# 메시지
# =========================================================

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    content = message.content.strip()

    uid = str(message.author.id)

    # =====================================================
    # 랜덤
    # =====================================================

    if content == "!운빨":

        await message.channel.send(random.choice(luck))

    elif content == "!오늘":

        await message.channel.send(random.choice(daily))

    # =====================================================
    # 확률
    # =====================================================

    elif content.startswith("!확률"):

        target = content[4:].strip()

        if not target:

            await message.channel.send(
                "사용법 : !확률 내용"
            )

            return

        percent = random.randint(0, 100)

        if percent <= 20:
            mood = "💀"

        elif percent <= 50:
            mood = "😐"

        elif percent <= 80:
            mood = "😊"

        else:
            mood = "💖"

        await message.channel.send(
            f"{target} 확률 : {percent}% {mood}"
        )
        
    # =====================================================
    # 돈
    # =====================================================

    elif content == "!돈":

        money = load_json(MONEY_FILE)

        if uid not in money:
            money[uid] = 1000
            save_json(MONEY_FILE, money)

        await message.channel.send(
            f"💰 현재 돈 : {money[uid]}원"
        )

    # =====================================================
    # 출석
    # =====================================================

    elif content == "!출석":

        checkin = load_json(CHECKIN_FILE)
        money = load_json(MONEY_FILE)

        today = str(datetime.date.today())

        if uid in checkin and checkin[uid] == today:

            await message.channel.send(
                "📅 오늘은 이미 출석했습니다!"
            )
            return

        checkin[uid] = today

        if uid not in money:
            money[uid] = 1000

        reward = random.randint(1000, 3000)

        money[uid] += reward

        save_json(CHECKIN_FILE, checkin)
        save_json(MONEY_FILE, money)

        await message.channel.send(
            f"""
📅 출석 완료!

💰 {reward}원 획득!
💵 현재 돈 : {money[uid]}원
"""
        )

    # =====================================================
    # 낚시대
    # =====================================================

    elif content == "!낚시대":

        rods = load_json(ROD_FILE)

        if uid not in rods:
            rods[uid] = 0
            save_json(ROD_FILE, rods)

        level = rods[uid]

        await message.channel.send(
            f"""
{get_rod_name(level)}

🎣 강화 수치 : +{level}
📈 강화 성공 확률 : {get_success_rate(level)}%
💰 강화 비용 : {get_upgrade_cost(level)}원
"""
        )

    # =====================================================
    # 강화
    # =====================================================

    elif content == "!강화":

        rods = load_json(ROD_FILE)
        money = load_json(MONEY_FILE)

        if uid not in rods:
            rods[uid] = 0

        if uid not in money:
            money[uid] = 1000

        level = rods[uid]

        if level >= MAX_LEVEL:

            await message.channel.send(
                "👑 이미 최대 강화입니다!"
            )
            return

        cost = get_upgrade_cost(level)

        if money[uid] < cost:

            await message.channel.send(
                "💸 돈 부족!"
            )
            return

        money[uid] -= cost

        success = get_success_rate(level)

        roll = random.randint(1, 100)

        if roll <= success:

            rods[uid] += 1

            save_json(ROD_FILE, rods)
            save_json(MONEY_FILE, money)

            await message.channel.send(
                f"""
✨ 강화 성공!

🎣 현재 강화 : +{rods[uid]}
💰 남은 돈 : {money[uid]}원
"""
            )

        else:

            save_json(MONEY_FILE, money)

            await message.channel.send(
                f"""
💀 강화 실패...

🎣 현재 강화 : +{rods[uid]}
"""
            )

    # =====================================================
    # 낚시
    # =====================================================

    elif content == "!낚시":

        rods = load_json(ROD_FILE)
        inventory = load_json(FISH_FILE)
        fish_count = load_json(FISH_COUNT_FILE)

        rod_level = rods.get(uid, 0)

        success = min(95, 50 + rod_level * 3)

        if random.randint(1, 100) > success:

            await message.channel.send(
                "💨 물고기를 놓쳤습니다..."
            )
            return

        fish = roll_fish(rod_level)

        if uid not in inventory:
            inventory[uid] = {}

        inventory[uid][fish["name"]] = (
            inventory[uid].get(fish["name"], 0) + 1
        )

        fish_count[uid] = fish_count.get(uid, 0) + 1

        save_json(FISH_FILE, inventory)
        save_json(FISH_COUNT_FILE, fish_count)

        rare = ""

        if fish["chance"] <= 4:
            rare = "\n🔥 희귀 물고기 등장!!"

        await message.channel.send(
            f"""
🎣 낚시 성공!

{fish['name']} 획득!
💰 판매 가격 : {fish['price']}원
{rare}
"""
        )

    # =====================================================
    # 인벤토리
    # =====================================================

    elif content == "!인벤":

        inventory = load_json(FISH_FILE)

        if uid not in inventory or not inventory[uid]:

            await message.channel.send(
                "🎒 인벤토리가 비어있습니다."
            )
            return

        msg = "🎒 물고기 인벤토리\n\n"

        for fish, count in inventory[uid].items():

            msg += f"{fish} x{count}\n"

        await message.channel.send(msg)

    # =====================================================
    # 판매
    # =====================================================

    elif content == "!판매":

        inventory = load_json(FISH_FILE)
        money = load_json(MONEY_FILE)

        if uid not in inventory or not inventory[uid]:

            await message.channel.send(
                "판매할 물고기가 없습니다."
            )
            return

        total = 0

        for fish_name, count in inventory[uid].items():

            for fish in FISHES:

                if fish["name"] == fish_name:

                    total += fish["price"] * count

        inventory[uid] = {}

        money[uid] = money.get(uid, 0) + total

        save_json(FISH_FILE, inventory)
        save_json(MONEY_FILE, money)

        await message.channel.send(
            f"""
💰 물고기 판매 완료!

+{total}원 획득!
💵 현재 돈 : {money[uid]}원
"""
        )

    # =====================================================
    # 자동 낚시
    # =====================================================

    elif content == "!자동낚시":

        auto = load_json(AUTO_FILE)

        auto[uid] = not auto.get(uid, False)

        save_json(AUTO_FILE, auto)

        state = "ON ✅" if auto[uid] else "OFF ❌"

        await message.channel.send(
            f"🎣 자동 낚시 : {state}"
        )

    # =====================================================
    # 보스 물고기
    # =====================================================

    elif content == "!보스":

        boss = load_json(BOSS_FILE)

        today = str(datetime.date.today())

        if boss.get("date") != today:

            boss["date"] = today
            boss["name"] = random.choice(BOSS_FISH)

            save_json(BOSS_FILE, boss)

        await message.channel.send(
            f"""
👹 오늘의 보스 물고기

{boss['name']}

처치 보상 : 50000원
"""
        )

    # =====================================================
    # 스킨 상점
    # =====================================================

    elif content == "!스킨상점":

        msg = "🛒 낚시대 스킨 상점\n\n"

        for skin, price in SKINS.items():

            msg += f"{skin} : {price}원\n"

        msg += "\n구매 : !스킨구매 이름"

        await message.channel.send(msg)

    # =====================================================
    # 스킨 구매
    # =====================================================

    elif content.startswith("!스킨구매"):

        money = load_json(MONEY_FILE)
        skins = load_json(SKIN_FILE)

        parts = content.split(maxsplit=1)

        if len(parts) < 2:

            await message.channel.send(
                "!스킨구매 이름"
            )
            return

        skin_name = parts[1]

        if skin_name not in SKINS:

            await message.channel.send(
                "존재하지 않는 스킨"
            )
            return

        price = SKINS[skin_name]

        if money.get(uid, 0) < price:

            await message.channel.send(
                "💸 돈 부족!"
            )
            return

        money[uid] -= price
        skins[uid] = skin_name

        save_json(MONEY_FILE, money)
        save_json(SKIN_FILE, skins)

        await message.channel.send(
            f"✨ {skin_name} 스킨 구매 완료!"
        )

    # =====================================================
    # 낚시 랭킹
    # =====================================================

    elif content == "!낚시랭킹":

        fish_count = load_json(FISH_COUNT_FILE)

        sorted_data = sorted(
            fish_count.items(),
            key=lambda x: x[1],
            reverse=True
        )

        msg = "🏆 낚시 랭킹 TOP 10\n\n"

        for i, (u, count) in enumerate(sorted_data[:10], 1):

            try:

                name = USER_MAP.get(int(u))

                if not name:
                    member = message.guild.get_member(int(u))
                    name = member.display_name if member else u

            except:
                name = u

            msg += f"{i}. {name} - {count}마리\n"

        await message.channel.send(msg)

    # =====================================================
    # 사용법
    # =====================================================

    elif content == "!사용법":

        await message.channel.send(
"""
📖 사용 가능한 명령어

🎣 낚시
!낚시
!자동낚시
!인벤
!판매
!보스
!낚시랭킹

🎣 강화
!낚시대
!강화

🛒 스킨
!스킨상점
!스킨구매 이름

📅 보상
!출석
!돈

🎲 랜덤
!운빨
!오늘
!확률 내용
        )

# =========================================================
# 자동 낚시 실행
# =========================================================

client.loop.create_task(auto_fishing_loop())

# =========================================================
# 실행
# =========================================================

client.run(TOKEN)