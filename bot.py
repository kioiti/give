import os
import json
import random
import datetime
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

DATA_FILE = "activity.json"
MONEY_FILE = "money.json"
ROD_FILE = "rod.json"
CHECKIN_FILE = "checkin.json"
PROTECT_FILE = "protect.json"

# ---------------- 유저 매핑 ----------------
USER_MAP = {
    1501525905833594900: "머래",
    261016503963353098: "계삭",
    464655989996519424: "마라콩",
    707895110972473345: "밈콩",
    435351384137662464: "지성콩",
    1004779456696688760: "미희여사",
    706114030061879296: "에빙",
}

# ---------------- 운빨 ----------------
luck = [
    "오늘 운: SSS급 🔥",
    "오늘 운: S급 👍",
    "오늘 운: A급 😊",
    "오늘 운: B급 😐",
    "오늘 운: C급 🤨",
    "오늘 운: D급 😵‍💫",
    "오늘 운: F급 💀",
    "오늘 운: 전설급 💸",
    "오늘 운: 버프 ON ⚡",
    "오늘 운: 너프 ON 📉",
    "오늘 운: 멘탈 흔들림 🫠",
    "오늘 운: 집중력 폭발 🎯",
    "오늘 운: 억까 구간",
    "오늘 운: 반응속도 +10%",
    "오늘 운: 판단력 상승 📈",
    "오늘 운: 그냥 오늘 레전드"
]

daily = [
    "오늘은 안정 플레이",
    "오늘은 무리 금지",
    "오늘은 집중각",
    "오늘은 감각 체크",
    "오늘은 천천히 가자",
    "오늘은 실수 줄이기",
    "오늘은 멘탈 관리",
    "오늘은 흐름 타기",
]

# ---------------- JSON ----------------
def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------- 강화 설정 ----------------
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


# ---------------- 시작 ----------------
@client.event
async def on_ready():
    print(f"{client.user} 로그인 완료")


# ---------------- 메시지 ----------------
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    content = message.content.strip()

    # ---------------- 랜덤 ----------------
    if content == "!운빨":
        await message.channel.send(random.choice(luck))

    elif content == "!오늘":
        await message.channel.send(random.choice(daily))

    # ---------------- 낚시대 ----------------
    elif content == "!낚시대":

        rods = load_json(ROD_FILE)

        uid = str(message.author.id)

        if uid not in rods:
            rods[uid] = 0
            save_json(ROD_FILE, rods)

        level = rods[uid]

        rod_name = get_rod_name(level)

        if level >= MAX_LEVEL:

            next_info = "👑 최대 강화 완료"

        else:

            cost = get_upgrade_cost(level)
            success = get_success_rate(level)

            next_info = (
                f"📈 다음 강화 확률 : {success}%\n"
                f"💰 강화 비용 : {cost}원"
            )

        await message.channel.send(
            f"""
{rod_name}

🎣 현재 강화 : +{level}

{next_info}
"""
        )

    # ---------------- 강화 ----------------
    elif content == "!강화":

        rods = load_json(ROD_FILE)
        money = load_json(MONEY_FILE)
        protect = load_json(PROTECT_FILE)

        uid = str(message.author.id)

        if uid not in rods:
            rods[uid] = 0

        if uid not in money:
            money[uid] = 1000

        if uid not in protect:
            protect[uid] = 0

        level = rods[uid]

        if level >= MAX_LEVEL:

            await message.channel.send(
                "👑 이미 +15 최대 강화입니다!"
            )

            return

        cost = get_upgrade_cost(level)

        if money[uid] < cost:

            await message.channel.send(
                f"💸 돈 부족! ({cost}원 필요)"
            )

            return

        money[uid] -= cost

        success_rate = get_success_rate(level)

        roll = random.randint(1, 100)

        # ---------------- 성공 ----------------
        if roll <= success_rate:

            rods[uid] += 1

            effects = [
                "✨ 반짝!",
                "🔥 뜨거운 기운이 감돈다!",
                "🌈 무지개 강화!",
                "⚡ 강력한 힘이 느껴진다!",
                "💥 초대박 성공!"
            ]

            effect = random.choice(effects)

            save_json(ROD_FILE, rods)
            save_json(MONEY_FILE, money)

            msg = (
                f"{effect}\n\n"
                f"✅ 강화 성공!\n"
                f"🎣 +{rods[uid]} {get_rod_name(rods[uid])}\n"
                f"💰 남은 돈 : {money[uid]}원"
            )

            if rods[uid] == 15:

                msg += (
                    f"\n\n👑 {message.author.display_name} 님이 "
                    f"+15 테런 낚시대를 달성했습니다!!!"
                )

            await message.channel.send(msg)

        # ---------------- 실패 ----------------
        else:

            # +12 이상 파괴
            if level >= 12:

                # 보호권 사용
                if protect[uid] > 0:

                    protect[uid] -= 1

                    save_json(PROTECT_FILE, protect)
                    save_json(MONEY_FILE, money)

                    await message.channel.send(
                        f"""
🛡 강화 실패!

보호권 사용으로 파괴 방지!

🛡 남은 보호권 : {protect[uid]}개
"""
                    )

                else:

                    rods[uid] = 0

                    save_json(ROD_FILE, rods)
                    save_json(MONEY_FILE, money)

                    await message.channel.send(
                        """
💀 강화 대폭발...

낚시대가 파괴되어
+0으로 돌아갔습니다.
"""
                    )

            # +10 ~ +11 하락 가능
            elif level >= 10:

                down = random.randint(1, 100)

                if down <= 40:

                    rods[uid] -= 1

                    save_json(ROD_FILE, rods)
                    save_json(MONEY_FILE, money)

                    await message.channel.send(
                        f"""
📉 강화 실패!

단계 하락...
🎣 현재 : +{rods[uid]}
"""
                    )

                else:

                    save_json(MONEY_FILE, money)

                    await message.channel.send(
                        f"""
❌ 강화 실패...

🎣 현재 : +{rods[uid]} 유지
"""
                    )

            else:

                save_json(MONEY_FILE, money)

                await message.channel.send(
                    f"""
❌ 강화 실패...

🎣 현재 : +{rods[uid]} 유지
"""
                )

    # ---------------- 보호권 ----------------
    elif content == "!보호권":

        protect = load_json(PROTECT_FILE)

        uid = str(message.author.id)

        if uid not in protect:
            protect[uid] = 0

        await message.channel.send(
            f"🛡 현재 보호권 : {protect[uid]}개"
        )

    # ---------------- 출석 ----------------
    elif content == "!출석":

        checkin = load_json(CHECKIN_FILE)
        money = load_json(MONEY_FILE)
        protect = load_json(PROTECT_FILE)

        uid = str(message.author.id)

        today = str(datetime.date.today())

        if uid in checkin and checkin[uid] == today:

            await message.channel.send(
                "📅 오늘은 이미 출석했습니다!"
            )

            return

        checkin[uid] = today

        if uid not in money:
            money[uid] = 1000

        if uid not in protect:
            protect[uid] = 0

        reward = random.randint(1000, 3000)

        money[uid] += reward

        bonus = ""

        # 20% 확률 보호권
        if random.randint(1, 100) <= 20:

            protect[uid] += 1

            bonus = "\n🛡 보호권 1개 획득!"

        save_json(CHECKIN_FILE, checkin)
        save_json(MONEY_FILE, money)
        save_json(PROTECT_FILE, protect)

        await message.channel.send(
            f"""
📅 출석 완료!

💰 {reward}원 획득!
💵 현재 돈 : {money[uid]}원
{bonus}
"""
        )

    # ---------------- 강화 랭킹 ----------------
    elif content == "!강화랭킹":

        rods = load_json(ROD_FILE)

        sorted_data = sorted(
            rods.items(),
            key=lambda x: x[1],
            reverse=True
        )

        msg = "🏆 강화 랭킹 TOP 10\n\n"

        for i, (u, level) in enumerate(sorted_data[:10], 1):

            try:

                name = USER_MAP.get(int(u))

                if not name:
                    member = message.guild.get_member(int(u))
                    name = member.display_name if member else u

            except:
                name = u

            msg += (
                f"{i}. {name} - "
                f"+{level} {get_rod_name(level)}\n"
            )

        await message.channel.send(msg)

    # ---------------- 확률 ----------------
    elif content.startswith("!확률"):

        target = content[4:].strip()

        if not target:
            await message.channel.send("!확률 내용")
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
            f"{target} 확률 {percent}% {mood}"
        )

    # ---------------- 돈 ----------------
    elif content == "!도박":

        money = load_json(MONEY_FILE)

        uid = str(message.author.id)

        if uid not in money:
            money[uid] = 1000

        amount = random.randint(-500, 1000)

        money[uid] += amount

        save_json(MONEY_FILE, money)

        if amount >= 0:

            await message.channel.send(
                f"💰 +{amount}원 획득! (현재 {money[uid]}원)"
            )

        else:

            await message.channel.send(
                f"💀 {abs(amount)}원 잃음... (현재 {money[uid]}원)"
            )

    elif content == "!돈":

        money = load_json(MONEY_FILE)

        uid = str(message.author.id)

        if uid not in money:

            money[uid] = 1000
            save_json(MONEY_FILE, money)

        await message.channel.send(
            f"💵 현재 돈 : {money[uid]}원"
        )

    # ---------------- 게임 ----------------
    elif content == "!주사위":

        await message.channel.send(
            f"🎲 {random.randint(1, 6)}"
        )

    elif content.startswith("!가위바위보"):

        try:
            user = content.split(" ")[1]

        except:

            await message.channel.send(
                "!가위바위보 가위/바위/보"
            )

            return

        bot = random.choice(["가위", "바위", "보"])

        if user == bot:

            result = "무승부"

        elif (
            (user == "가위" and bot == "보")
            or (user == "바위" and bot == "가위")
            or (user == "보" and bot == "바위")
        ):

            result = "승리"

        else:

            result = "패배"

        await message.channel.send(
            f"너:{user} / 봇:{bot} → {result}"
        )

    elif content.startswith("!숫자"):

        answer = random.randint(0, 5)

        try:
            guess = int(content.split(" ")[1])

        except:

            await message.channel.send("!숫자 3")
            return

        await message.channel.send(
            "정답 🎉"
            if guess == answer
            else f"틀림 💀 ({answer})"
        )

    # ---------------- 랭킹 ----------------
    data = load_json(DATA_FILE)

    uid = str(message.author.id)

    data[uid] = data.get(uid, 0) + 1

    save_json(DATA_FILE, data)

    if content == "!랭킹":

        sorted_data = sorted(
            data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        msg = "📊 채팅 랭킹\n\n"

        for i, (u, cnt) in enumerate(sorted_data[:5], 1):

            try:

                name = USER_MAP.get(int(u))

                if not name:
                    member = message.guild.get_member(int(u))
                    name = member.display_name if member else u

            except:
                name = u

            msg += f"{i}. {name} - {cnt}\n"

        await message.channel.send(msg)

    elif content == "!내순위":

        sorted_data = sorted(
            data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for i, (u, cnt) in enumerate(sorted_data, 1):

            if u == uid:

                await message.channel.send(
                    f"🏆 {i}등 ({cnt})"
                )

                return

    # ---------------- 사용법 ----------------
    elif content == "!사용법":

        await message.channel.send(
"""📖 사용 가능한 명령어

🎣 낚시대 강화
!낚시대
!강화
!강화랭킹
!보호권

📅 보상
!출석

💰 돈 시스템
!도박
!돈

🎲 랜덤
!운빨
!오늘
!확률

🎮 게임
!주사위
!가위바위보 가위/바위/보
!숫자 3

📊 랭킹
!랭킹
!내순위
"""
        )

client.run(TOKEN)