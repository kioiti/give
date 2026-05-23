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
GAME_FILE = "game.json"


# ---------------- 데이터 ----------------
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------- 밈 ----------------
luck = [
    "오늘 운: SSS급 🔥 숨만 쉬어도 이득",
    "오늘 운: S급 👍 안정적인 떡상",
    "오늘 운: A급 😊 무난하게 좋음",
    "오늘 운: B급 😐 평범",
    "오늘 운: C급 🤨 살짝 꼬임",
    "오늘 운: D급 😵‍💫 조심해야 함",
    "오늘 운: F급 💀 오늘은 쉬자",
    "오늘 운: 전설급 💸 돈 줍는 날",
    "오늘 운: 버프 ON ⚡",
    "오늘 운: 너프 ON 📉",
    "오늘 운: 멘탈 흔들림 🫠",
    "오늘 운: 집중력 폭발 🎯",
    "오늘 운: 팀운 SSS (본인 제외)",
    "오늘 운: 억까 구간 진입 🚨",
    "오늘 운: 반응속도 +10%",
    "오늘 운: 판단력 상승 📈",
    "오늘 운: 실수 2배 증가",
    "오늘 운: 오늘은 감각 좋음",
    "오늘 운: 그냥 웃고 넘어가라",
    "오늘 운: 레전드 하루"
]

whine = [
    "이건 게임이 아니라 시험이다",
    "내 손이 오늘 잠수함 탔다",
    "이건 억까다 진짜",
    "점프가 말을 안 듣는다",
    "내 입력이 늦게 도착함",
    "이건 물리엔진 문제다",
    "팀원이 아니라 고난이다",
    "왜 나만 이런 상황이냐",
    "벽이랑 싸우는 중",
    "이건 실력 문제가 아니다",
    "오늘은 손가락이 파업",
    "상대만 게임함",
    "나만 슬로우모션",
    "이건 설계가 이상하다",
    "멘탈이 먼저 나감",
    "오늘은 접는 게 맞다",
    "이건 진짜 아니다",
    "왜 계속 미끄러지냐",
    "게임이 나를 싫어함",
    "그냥 웃자..."
]

daily = [
    "오늘은 안정 플레이가 답이다",
    "오늘은 욕심 금지",
    "오늘은 집중하면 올라간다",
    "오늘은 감 잡는 날",
    "오늘은 한 판씩 천천히",
    "오늘은 실수 줄이기",
    "오늘은 멘탈 관리",
    "오늘은 흐름 타는 날",
    "오늘은 무리하지 말자",
    "오늘은 연습 느낌",
    "오늘은 각 좋다",
    "오늘은 판단이 중요",
    "오늘은 침착하게",
    "오늘은 안정이 최고",
    "오늘은 욕심내면 망함",
    "오늘은 집중하면 승률 상승",
    "오늘은 초반이 중요",
    "오늘은 무난하게 가자",
    "오늘은 실험 금지",
    "오늘은 깔끔하게"
]

reaction = [
    "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
    "이건 레전드다",
    "ㅋㅋㅋㅋ 개웃기네",
    "이건 인정",
    "와 이건 심했다",
    "공감 100%",
    "이건 저장각",
    "미쳤다 ㅋㅋㅋㅋ",
    "이건 억까",
    "진짜 현실 반영",
    "ㅋㅋㅋㅋㅋㅋㅋㅋ",
    "이건 나도 당함",
    "와 개빡친다",
    "웃기면서 슬프다",
    "이건 레전드 상황",
    "ㅋㅋㅋㅋㅋㅋ 못참음",
    "이건 게임이 문제",
    "진짜 공감됨",
    "이건 웃겨서 저장",
    "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ"
]


# ---------------- 게임 데이터 ----------------
games = load_json(GAME_FILE)


# ---------------- 준비 ----------------
@client.event
async def on_ready():
    print(f"{client.user} 로그인 완료")


# ---------------- 메시지 ----------------
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user = str(message.author.id)

    # ---------------- 활동 기록 ----------------
    data = load_json(DATA_FILE)
    data[user] = data.get(user, 0) + 1
    save_json(DATA_FILE, data)

    content = message.content.strip()


    # ---------------- 밈 ----------------
    if content == "!운빨":
        await message.channel.send(random.choice(luck))
        return

    if content == "!징징":
        await message.channel.send(random.choice(whine))
        return

    if content == "!오늘":
        await message.channel.send(random.choice(daily))
        return

    if content == "!반응":
        await message.channel.send(random.choice(reaction))
        return


    # ---------------- 🎲 미니게임 ----------------

    # 주사위
    if content == "!주사위":
        await message.channel.send(f"🎲 결과: {random.randint(1, 6)}")
        return

    # 가위바위보
    if content.startswith("!가위바위보"):
        choices = ["가위", "바위", "보"]
        bot = random.choice(choices)

        try:
            user_choice = content.split(" ")[1]
        except:
            await message.channel.send("사용법: !가위바위보 가위/바위/보")
            return

        if user_choice not in choices:
            await message.channel.send("가위 / 바위 / 보 중 하나만 입력")
            return

        if user_choice == bot:
            result = "무승부 🤝"
        elif (user_choice == "가위" and bot == "보") or \
             (user_choice == "바위" and bot == "가위") or \
             (user_choice == "보" and bot == "바위"):
            result = "승리 🎉"
        else:
            result = "패배 💀"

        await message.channel.send(f"너: {user_choice}\n봇: {bot}\n결과: {result}")
        return


    # 숫자 맞추기 (0~5 간단 버전)
    if content.startswith("!숫자"):
        answer = random.randint(0, 5)

        try:
            guess = int(content.split(" ")[1])
        except:
            await message.channel.send("사용법: !숫자 3 (0~5)")
            return

        if guess == answer:
            await message.channel.send(f"정답 🎉 ({answer})")
        else:
            await message.channel.send(f"틀림 💀 정답은 {answer}")
        return


    # ---------------- 📊 랭킹 ----------------
    if content == "!랭킹":
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        msg = "📊 서버 랭킹 TOP 5\n"
        for i, (uid, count) in enumerate(sorted_data[:5], 1):
            user_obj = await client.fetch_user(int(uid))
            msg += f"{i}. {user_obj.name} - {count}개\n"

        await message.channel.send(msg)
        return


    if content == "!내순위":
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        for i, (uid, count) in enumerate(sorted_data, 1):
            if uid == user:
                await message.channel.send(f"🏆 당신은 {i}등 ({count}개)")
                return


    # ---------------- ❓ 사용법 ----------------
    if content == "!사용법":
        await message.channel.send(
            """
🎮 **봇 사용법**

😂 밈
!운빨
!징징
!오늘
!반응

🎲 미니게임
!주사위
!가위바위보 가위/바위/보
!숫자 0~5

📊 랭킹
!랭킹
!내순위

💡 채팅 많이 하면 랭킹 올라감
"""
        )
        return


client.run(TOKEN)