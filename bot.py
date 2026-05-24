import os
import json
import random
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

DATA_FILE = "activity.json"
MONEY_FILE = "money.json"

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


# ---------------- 밈 ----------------
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

whine = [
    "야 또 잠수냐?",
    "왜 또 안 보이냐",
    "게임 안 하냐?",
    "너 지금 숨 쉬는 중?",
    "AFK 장인",
    "존재감 어디감",
    "접속 버튼 눌러라",
    "너 없어서 조용하다",
    "살아있냐?",
    "채팅 금지 상태냐?",
    "이건 좀 심하다",
    "너 어디갔냐",
    "잠수함 출항함?",
    "오늘도 로그아웃?",
    "귀신됨?"
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
    "오늘은 욕심 금지",
    "오늘은 연습 느낌",
    "오늘은 각 좋음",
    "오늘은 침착하게",
    "오늘은 안정이 최고",
    "오늘은 무난하게",
    "오늘은 실험 금지"
]

reaction = [
    "ㅋㅋㅋㅋㅋㅋㅋㅋ",
    "이건 레전드",
    "개웃기네",
    "인정",
    "와 심했다",
    "공감됨",
    "이건 저장각",
    "미쳤다 ㅋㅋ",
    "억까다",
    "현실 반영됨",
    "ㅋㅋㅋㅋ",
    "나도 당함",
    "개빡침",
    "웃긴데 슬픔",
    "레전드 상황"
]

fortune = [
    "오늘은 뭘 해도 잘 풀린다 🍀",
    "오늘은 억까 조심",
    "곧 좋은 일 생김",
    "오늘은 잠이나 자라 😴",
    "오늘은 집중력 미쳤다",
    "오늘은 현질 금지",
    "오늘은 게임각이다",
    "오늘은 운 다 씀",
]

tiers = [
    "브론즈",
    "실버",
    "골드",
    "플래티넘",
    "다이아",
    "마스터",
    "그랜드마스터",
    "챌린저"
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

    # ---------------- 밈 ----------------
    if content == "!운빨":
        await message.channel.send(random.choice(luck))

    elif content == "!징징":
        await message.channel.send(random.choice(whine))

    elif content == "!오늘":
        await message.channel.send(random.choice(daily))

    elif content == "!반응":
        await message.channel.send(random.choice(reaction))

    elif content == "!운세":
        await message.channel.send(random.choice(fortune))

    elif content == "!티어":
        await message.channel.send(
            f"🏆 오늘의 티어 : {random.choice(tiers)}"
        )

    # ---------------- 강화 시스템 ----------------
    elif content == "!강화":
        percent = random.randint(1, 100)

        if percent <= 5:
            msg = "💥 강화 대폭발"
        elif percent <= 40:
            msg = "❌ 강화 실패"
        elif percent <= 90:
            msg = "✅ 강화 성공"
        else:
            msg = "🔥 초대박 강화 성공"

        await message.channel.send(msg)

    # ---------------- 호감도 ----------------
    elif content.startswith("!호감도"):
        target = content[5:].strip()

        if not target:
            await message.channel.send("!호감도 @닉네임")
            return

        percent = random.randint(0, 100)

        if percent <= 20:
            mood = "💀 거의 원수급"
        elif percent <= 50:
            mood = "😐 애매함"
        elif percent <= 80:
            mood = "😊 꽤 친함"
        else:
            mood = "💖 찐호감"

        await message.channel.send(
            f"{target} 호감도 : {percent}% {mood}"
        )

    # ---------------- 도박 시스템 ----------------
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
        await message.channel.send(f"🎲 {random.randint(1,6)}")

    elif content.startswith("!가위바위보"):
        try:
            user = content.split(" ")[1]
        except:
            await message.channel.send("!가위바위보 가위/바위/보")
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

        await message.channel.send(f"너:{user} / 봇:{bot} → {result}")

    elif content.startswith("!숫자"):
        answer = random.randint(0, 5)

        try:
            guess = int(content.split(" ")[1])
        except:
            await message.channel.send("!숫자 3")
            return

        await message.channel.send(
            "정답 🎉" if guess == answer else f"틀림 💀 ({answer})"
        )

    # ---------------- 랭킹 ----------------
    data = load_json(DATA_FILE)

    uid = str(message.author.id)
    data[uid] = data.get(uid, 0) + 1

    save_json(DATA_FILE, data)

    if content == "!랭킹":
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        msg = "📊 채팅 랭킹\n"

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
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        for i, (u, cnt) in enumerate(sorted_data, 1):
            if u == uid:
                await message.channel.send(f"🏆 {i}등 ({cnt})")
                return

    # ---------------- 사용법 ----------------
    elif content == "!사용법":
        await message.channel.send(
"""📖 사용 가능한 명령어

🎲 랜덤 / 밈
!운빨 → 오늘 운 확인
!운세 → 랜덤 운세
!징징 → 징징 멘트
!오늘 → 오늘의 상태
!반응 → 랜덤 반응
!티어 → 오늘의 티어

🎮 게임
!주사위
!가위바위보 가위/바위/보
!숫자 3

🔥 강화 / 호감도
!강화
!호감도 @닉네임

💰 돈 시스템
!도박
!돈

📊 랭킹
!랭킹
!내순위
"""
        )


client.run(TOKEN)