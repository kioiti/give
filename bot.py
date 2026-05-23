import os
import json
import random
import discord
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

DATA_FILE = "activity.json"


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


# ---------------- 상태 ----------------
last_seen = {}
next_ping = {}


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
    client.loop.create_task(idle_checker())


# ---------------- 메시지 ----------------
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id
    now = datetime.now()

    # 마지막 활동 기록
    last_seen[user_id] = now

    # 처음 보면 오래된 상태 → 바로 체크되게 초기값 세팅
    if user_id not in next_ping:
        next_ping[user_id] = now + timedelta(hours=random.randint(1, 5))

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


    # ---------------- 게임 ----------------
    elif content == "!주사위":
        await message.channel.send(f"🎲 {random.randint(1,6)}")

    elif content.startswith("!가위바위보"):
        try:
            user = content.split(" ")[1]
        except:
            await message.channel.send("!가위바위보 가위/바위/보")
            return

        bot = random.choice(["가위","바위","보"])

        if user == bot:
            result = "무승부"
        elif (user=="가위" and bot=="보") or (user=="바위" and bot=="가위") or (user=="보" and bot=="바위"):
            result = "승리"
        else:
            result = "패배"

        await message.channel.send(f"너:{user} / 봇:{bot} → {result}")

    elif content.startswith("!숫자"):
        answer = random.randint(0,5)
        try:
            guess = int(content.split(" ")[1])
        except:
            await message.channel.send("!숫자 3")
            return

        await message.channel.send("정답 🎉" if guess == answer else f"틀림 💀 ({answer})")


    # ---------------- 랭킹 ----------------
    data = load_json(DATA_FILE)
    uid = str(message.author.id)
    data[uid] = data.get(uid, 0) + 1
    save_json(DATA_FILE, data)

    if content == "!랭킹":
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        msg = "📊 랭킹\n"

        for i, (u, cnt) in enumerate(sorted_data[:5], 1):
            name = USER_MAP.get(int(u), u)
            msg += f"{i}. {name} - {cnt}\n"

        await message.channel.send(msg)

    elif content == "!내순위":
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        for i, (u, cnt) in enumerate(sorted_data, 1):
            if u == uid:
                await message.channel.send(f"🏆 {i}등 ({cnt})")
                return

    elif content == "!사용법":
        await message.channel.send(
"""😂 !운빨 !징징 !오늘 !반응
🎲 !주사위 !가위바위보 !숫자
📊 !랭킹 !내순위"""
        )


# ---------------- 🔥 잠수 시스템 ----------------
async def idle_checker():
    await client.wait_until_ready()

    while not client.is_closed():
        now = datetime.now()

        for uid, name in USER_MAP.items():

            # 마지막 활동 없으면 오래된 상태 처리
            last = last_seen.get(uid, now - timedelta(hours=10))

            # next_ping 없으면 초기화
            if uid not in next_ping:
                next_ping[uid] = now + timedelta(hours=random.randint(1, 5))
                continue

            # 🚨 핵심 1: 아직 시간이 안 됐으면 절대 실행 안 함
            if now < next_ping[uid]:
                continue

            # 메시지 리스트
            messages = [
                f"{name}아 뭐하냐 또 잠수냐?",
                f"{name}아 ㅋㅋ 또 안 보이네",
                f"{name}아 이걸 잔다고?",
                f"{name}아 진짜 말안댄다.",
                f"{name}아 언제와? 왜 안와? 어디야?",
                f"{name}아 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며",
                f"{name}아 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며",
                f"{name}아 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며 사랑한다며",
                f"{name}아 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며",
                f"{name}아 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며",
                f"{name}아 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며 나밖에 없다며",
                f"{name} 살아있냐?",
                f"{name} 어디갔냐",
                f"{name} 일어나라 테런 켜라.",
                f"{name} 오늘도 잠수냐?",
                f"{name} 채팅 금지 상태냐?",
                f"{name} 너 어디갔냐",
                f"{name} 잠수함 출항함?",
            ]

            msg = random.choice(messages)

            # 🚨 핵심 2: 한 번만 보내고 끝
            try:
                for ch in client.get_all_channels():
                    if hasattr(ch, "send"):
                        await ch.send(msg)
                        break
            except:
                pass

            # 🚨 핵심 3: 무조건 다음 알림 1~5시간 뒤로 밀기
            next_ping[uid] = now + timedelta(hours=random.randint(1, 5))

        await asyncio.sleep(60)


client.run(TOKEN)