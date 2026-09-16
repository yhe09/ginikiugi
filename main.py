import streamlit as st
import streamlit.components.v1 as components
import random
import time
import json
import html

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="기니키우기",
    page_icon="🐹",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "started": False,
    "name": "",
    "hunger": 78,
    "water": 82,
    "clean": 92,
    "happy": 86,
    "poop": [],
    "message": "오늘도 잘 부탁해! 🐹",
    "last_update": time.time(),
    "last_poop": time.time(),
    "feed_count": 0,
    "water_count": 0,
    "clean_count": 0,
    "pet_count": 0,
    "day": 1,
    "coins": 30,
    "action": "idle",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# TIME / STATUS UPDATE
# ============================================================

def update_pet_state():
    now = time.time()

    elapsed = now - st.session_state.last_update

    # 너무 빠르게 감소하지 않도록 30초 단위
    if elapsed >= 30:
        ticks = int(elapsed // 30)

        st.session_state.hunger = max(
            0,
            st.session_state.hunger - 2 * ticks
        )

        st.session_state.water = max(
            0,
            st.session_state.water - 2 * ticks
        )

        st.session_state.clean = max(
            0,
            st.session_state.clean - 1 * ticks
        )

        st.session_state.happy = max(
            0,
            st.session_state.happy - 1 * ticks
        )

        st.session_state.last_update = now

    # 일정 시간이 지나면 배설물 생성
    poop_elapsed = now - st.session_state.last_poop

    if poop_elapsed >= 90:
        number = min(
            int(poop_elapsed // 90),
            3
        )

        for _ in range(number):
            if len(st.session_state.poop) < 10:
                st.session_state.poop.append({
                    "x": random.randint(15, 80),
                    "y": random.randint(48, 78),
                })

        st.session_state.clean = max(
            0,
            st.session_state.clean - number * 5
        )

        st.session_state.last_poop = now


update_pet_state()


# ============================================================
# HELPER
# ============================================================

def clamp(value):
    return max(0, min(100, int(value)))


def overall_mood():
    avg = (
        st.session_state.hunger
        + st.session_state.water
        + st.session_state.clean
        + st.session_state.happy
    ) / 4

    if avg >= 85:
        return "최고로 행복해요!", "♡"
    elif avg >= 70:
        return "기분이 좋아요!", "♡"
    elif avg >= 50:
        return "평범한 하루예요.", "·"
    elif avg >= 30:
        return "조금 돌봐주세요!", "!"
    else:
        return "많이 돌봐줘야 해요!", "!"


def guinea_expression():
    avg = (
        st.session_state.hunger
        + st.session_state.water
        + st.session_state.clean
        + st.session_state.happy
    ) / 4

    if avg >= 80:
        return "happy"

    if st.session_state.hunger < 30:
        return "hungry"

    if st.session_state.water < 30:
        return "thirsty"

    if st.session_state.clean < 30:
        return "sad"

    return "normal"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Jua&family=Press+Start+2P&display=swap');

html, body, [class*="css"] {
    font-family: 'Jua', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 10%, #fffaf0 0%, transparent 30%),
        linear-gradient(
            180deg,
            #f7ead7 0%,
            #f1dfc5 100%
        );
    color: #5c4635;
}

.block-container {
    max-width: 780px;
    padding-top: 28px;
    padding-bottom: 40px;
}

/* Streamlit 기본 요소 숨기기 */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* 제목 */

.game-title {
    text-align: center;
    font-family: 'Jua', sans-serif;
    font-size: 54px;
    color: #765238;
    letter-spacing: -2px;
    margin-bottom: 0;
    text-shadow:
        2px 2px 0 #ead3b3;
}

.game-subtitle {
    text-align: center;
    color: #9c8063;
    font-size: 15px;
    margin-top: -3px;
    margin-bottom: 22px;
}

/* 상단 날짜 카드 */

.day-card {
    background: #fff8ec;
    border: 3px solid #dec7a7;
    border-radius: 18px;
    padding: 11px 17px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 0 #d0b796;
    margin-bottom: 18px;
}

.day-left {
    font-size: 14px;
    color: #80654d;
}

.coin {
    color: #9a7542;
    font-size: 14px;
}

/* 케이지 */

.cage-wrapper {
    background: #d4b58c;
    border-radius: 30px;
    padding: 10px;
    box-shadow:
        0 7px 0 #b9966c,
        0 13px 22px rgba(105, 76, 46, 0.12);
    margin-bottom: 20px;
}

.cage {
    position: relative;
    height: 430px;
    overflow: hidden;
    border-radius: 22px;
    border: 5px solid #a98257;

    background:
        linear-gradient(
            rgba(255,255,255,.08),
            rgba(255,255,255,.08)
        ),
        repeating-linear-gradient(
            0deg,
            #dfc19b 0px,
            #dfc19b 5px,
            #d9b98f 5px,
            #d9b98f 9px
        );
}

/* 뒤쪽 벽 */

.cage-wall {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    height: 110px;

    background:
        repeating-linear-gradient(
            90deg,
            rgba(255,255,255,.10) 0px,
            rgba(255,255,255,.10) 3px,
            transparent 3px,
            transparent 35px
        ),
        #e8d2b2;

    border-bottom: 5px solid #c4a178;
}

/* 바닥 */

.floor {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 105px;

    background:
        repeating-linear-gradient(
            0deg,
            #d1ad7f 0px,
            #d1ad7f 4px,
            #c7a274 4px,
            #c7a274 8px
        );

    border-top: 4px solid #b99062;
}

/* 케이지 철망 */

.bar {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 3px;
    background: rgba(112, 82, 54, 0.18);
}

.bar1 { left: 18%; }
.bar2 { left: 38%; }
.bar3 { left: 58%; }
.bar4 { left: 78%; }

.horizontal-bar {
    position: absolute;
    left: 0;
    right: 0;
    height: 3px;
    background: rgba(112, 82, 54, 0.14);
}

.horizontal1 { top: 28%; }
.horizontal2 { top: 50%; }
.horizontal3 { top: 72%; }

/* 건초 */

.hay {
    position: absolute;
    right: 30px;
    bottom: 45px;
    font-size: 52px;
    filter: drop-shadow(2px 3px 0 rgba(95, 64, 38, .18));
}

/* 집 */

.house {
    position: absolute;
    left: 35px;
    bottom: 45px;
    width: 105px;
    height: 75px;
    background: #b98254;
    border: 5px solid #8e623f;
    border-radius: 8px 8px 15px 15px;
    box-shadow: 0 6px 0 #765037;
}

.house-roof {
    position: absolute;
    width: 0;
    height: 0;
    border-left: 65px solid transparent;
    border-right: 65px solid transparent;
    border-bottom: 55px solid #9e704b;
    left: -13px;
    top: -51px;
}

.house-door {
    position: absolute;
    bottom: 0;
    left: 34px;
    width: 37px;
    height: 48px;
    background: #5f4836;
    border-radius: 22px 22px 0 0;
}

/* 물병 */

.water-bottle {
    position: absolute;
    right: 135px;
    top: 105px;
    width: 42px;
    height: 68px;
    background: #c9e2e4;
    border: 4px solid #799da0;
    border-radius: 9px;
    opacity: .9;
}

.water-top {
    position: absolute;
    width: 17px;
    height: 13px;
    background: #78999a;
    top: -14px;
    left: 8px;
    border-radius: 4px;
}

.water-nozzle {
    position: absolute;
    width: 36px;
    height: 8px;
    background: #78999a;
    right: -32px;
    bottom: 7px;
    transform: rotate(25deg);
}

/* 먹이그릇 */

.food-bowl {
    position: absolute;
    left: 180px;
    bottom: 45px;
    width: 70px;
    height: 30px;
    background: #d89472;
    border: 4px solid #9f624a;
    border-radius: 8px 8px 25px 25px;
}

.food {
    position: absolute;
    left: 190px;
    bottom: 63px;
    font-size: 23px;
}

/* 기니피그 */

.guinea-wrap {
    position: absolute;
    left: 50%;
    bottom: 92px;

    animation:
        guineaWalk 8s ease-in-out infinite alternate,
        guineaBob .55s steps(2) infinite;
}

@keyframes guineaWalk {
    0% {
        transform: translateX(-190px);
    }

    45% {
        transform: translateX(-45px);
    }

    100% {
        transform: translateX(175px);
    }
}

@keyframes guineaBob {
    0% {
        margin-bottom: 0px;
    }

    100% {
        margin-bottom: 4px;
    }
}

.guinea {
    position: relative;
    width: 135px;
    height: 105px;
}

/* 픽셀풍 기니피그 몸 */

.guinea-body {
    position: absolute;
    left: 20px;
    top: 25px;
    width: 100px;
    height: 65px;

    background:
        linear-gradient(
            90deg,
            #f0d5aa 0%,
            #ead0a7 65%,
            #d6ad7c 66%,
            #d6ad7c 100%
        );

    border-radius: 45% 48% 42% 45%;

    border: 5px solid #9c704b;

    box-shadow:
        5px 6px 0 #b58960;
}

/* 머리 */

.guinea-head {
    position: absolute;
    left: 0;
    top: 18px;
    width: 70px;
    height: 72px;

    background: #eed2a7;

    border: 5px solid #9c704b;
    border-radius: 45% 48% 48% 45%;

    z-index: 4;
}

/* 얼굴 흰 무늬 */

.face-mark {
    position: absolute;
    left: 18px;
    top: 3px;
    width: 28px;
    height: 63px;

    background: #fff4df;

    border-radius: 50%;
}

/* 귀 */

.ear {
    position: absolute;
    width: 25px;
    height: 25px;
    background: #d7967f;
    border: 4px solid #8f624d;
    border-radius: 50%;
    z-index: 3;
}

.ear-left {
    left: -7px;
    top: 8px;
}

.ear-right {
    right: -4px;
    top: 10px;
}

/* 눈 */

.eye {
    position: absolute;
    width: 9px;
    height: 9px;
    background: #473429;
    border-radius: 50%;
    top: 34px;
    z-index: 6;
}

.eye-left {
    left: 13px;
}

.eye-right {
    right: 12px;
}

/* 코 */

.nose {
    position: absolute;
    left: 29px;
    bottom: 13px;
    width: 12px;
    height: 9px;
    background: #7f4e45;
    border-radius: 50%;
    z-index: 6;
}

/* 발 */

.foot {
    position: absolute;
    bottom: -3px;
    width: 28px;
    height: 13px;
    background: #d79c82;
    border: 3px solid #90634c;
    border-radius: 50%;
    z-index: 5;
}

.foot1 {
    left: 37px;
}

.foot2 {
    right: 10px;
}

/* 상태 말풍선 */

.speech {
    position: absolute;
    top: 28px;
    left: 50%;
    transform: translateX(-50%);
    background: #fffaf1;
    border: 3px solid #d4b993;
    border-radius: 16px;
    padding: 8px 14px;
    color: #76563f;
    font-size: 14px;
    white-space: nowrap;
    box-shadow: 0 3px 0 #c3a57f;
    z-index: 20;
}

.speech:after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    margin-left: -8px;

    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 10px solid #d4b993;
}

/* 배설물 */

.poop {
    position: absolute;
    font-size: 16px;
    z-index: 5;
}

/* 상태 */

.status-box {
    background: #fff9ef;
    border: 3px solid #dfc9ab;
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 18px;
    box-shadow: 0 5px 0 #d1b897;
}

.status-name {
    font-size: 22px;
    color: #765238;
    margin-bottom: 12px;
}

.mini-status {
    color: #8b7158;
    font-size: 13px;
    margin-bottom: 4px;
}

.progress {
    height: 12px;
    background: #eadbc5;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 11px;
}

.progress-fill {
    height: 100%;
    border-radius: 20px;
}

/* 버튼 */

div.stButton > button {
    width: 100%;
    min-height: 56px;

    background: #fff9ef;
    color: #765238;

    border: 3px solid #d8bea0;
    border-radius: 17px;

    font-family: 'Jua', sans-serif;
    font-size: 16px;

    box-shadow: 0 4px 0 #c2a482;

    transition: all .12s ease;
}

div.stButton > button:hover {
    background: #f7ead7;
    border-color: #b99972;
    transform: translateY(2px);
    box-shadow: 0 2px 0 #c2a482;
}

div.stButton > button:active {
    transform: translateY(4px);
    box-shadow: none;
}

/* 안내 */

.notice {
    text-align: center;
    background: #fff9ef;
    border: 2px dashed #d6b995;
    border-radius: 17px;
    padding: 12px;
    color: #987c60;
    font-size: 14px;
    margin: 18px 0;
}

/* 푸터 */

.footer {
    text-align: center;
    color: #ae9579;
    font-size: 12px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.started:

    st.markdown(
        '<div class="game-title">🐹 기니키우기</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="game-subtitle">작고 포근한 친구와 함께하는 작은 하루</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="status-box" style="text-align:center; padding:30px;">
        <div style="font-size:75px;">🐹</div>
        <div style="
            font-size:24px;
            color:#765238;
            margin-top:10px;
        ">
            새로운 기니피그가 찾아왔어요!
        </div>

        <div style="
            color:#987c60;
            font-size:14px;
            margin-top:8px;
            line-height:1.7;
        ">
            이름을 지어주고<br>
            나만의 작은 친구를 돌봐주세요 ♡
        </div>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(
        "기니피그 이름",
        placeholder="예: 콩이, 두부, 감자, 밤이..."
    )

    if st.button("🐹 기니피그 만나기"):

        if name.strip():

            st.session_state.started = True
            st.session_state.name = name.strip()
            st.session_state.message = (
                f"{name.strip()}가 당신을 만났어요! ♡"
            )

            st.rerun()

        else:

            st.warning("먼저 기니피그 이름을 지어주세요! 🐹")

    st.markdown(
        '<div class="footer">♡ 소중하게 돌봐주세요 ♡</div>',
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# MAIN
# ============================================================

st.markdown(
    '<div class="game-title">🐹 기니키우기</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">오늘도 ' +
    html.escape(st.session_state.name) +
    '와 함께하는 하루</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    f"""
    <div class="day-card">
        <div class="day-left">
            🌱 DAY {st.session_state.day}
        </div>

        <div class="coin">
            🪙 {st.session_state.coins}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CAGE
# ============================================================

poop_html = ""

for p in st.session_state.poop:

    poop_html += f"""
    <div class="poop"
         style="left:{p['x']}%; top:{p['y']}%;">
        🟤
    </div>
    """


expression = guinea_expression()

if expression == "happy":
    speech = "히히! 오늘 기분 최고야 ♡"
elif expression == "hungry":
    speech = "배고파... 🥬"
elif expression == "thirsty":
    speech = "목말라... 💧"
elif expression == "sad":
    speech = "케이지가 조금 더러워... 🥺"
else:
    speech = st.session_state.message


cage_html = f"""
<div class="cage-wrapper">

<div class="cage">

    <div class="cage-wall"></div>

    <div class="bar bar1"></div>
    <div class="bar bar2"></div>
    <div class="bar bar3"></div>
    <div class="bar bar4"></div>

    <div class="horizontal-bar horizontal1"></div>
    <div class="horizontal-bar horizontal2"></div>
    <div class="horizontal-bar horizontal3"></div>

    <div class="floor"></div>

    <!-- 집 -->
    <div class="house">
        <div class="house-roof"></div>
        <div class="house-door"></div>
    </div>

    <!-- 물병 -->
    <div class="water-bottle">
        <div class="water-top"></div>
        <div class="water-nozzle"></div>
    </div>

    <!-- 먹이 -->
    <div class="food-bowl"></div>
    <div class="food">🥬</div>

    <!-- 건초 -->
    <div class="hay">🌾</div>

    <!-- 배설물 -->
    {poop_html}

    <!-- 말풍선 -->
    <div class="speech">
        {html.escape(speech)}
    </div>

    <!-- 기니피그 -->
    <div class="guinea-wrap">

        <div class="guinea">

            <div class="guinea-body"></div>

            <div class="ear ear-left"></div>
            <div class="ear ear-right"></div>

            <div class="guinea-head">
                <div class="face-mark"></div>

                <div class="eye eye-left"></div>
                <div class="eye eye-right"></div>

                <div class="nose"></div>
            </div>

            <div class="foot foot1"></div>
            <div class="foot foot2"></div>

        </div>

    </div>

</div>

</div>
"""

st.markdown(cage_html, unsafe_allow_html=True)


# ============================================================
# STATUS
# ============================================================

mood_text, mood_symbol = overall_mood()

st.markdown(
    f"""
    <div class="status-box">

        <div class="status-name">
            🐹 {html.escape(st.session_state.name)}
        </div>

        <div style="
            color:#9a7d60;
            font-size:13px;
            margin-bottom:15px;
        ">
            {mood_symbol} {mood_text}
        </div>

        <div class="mini-status">
            🥬 배부름　{st.session_state.hunger}/100
        </div>

        <div class="progress">
            <div class="progress-fill"
                 style="
                    width:{st.session_state.hunger}%;
                    background:#d89a72;
                 ">
            </div>
        </div>

        <div class="mini-status">
            💧 수분　{st.session_state.water}/100
        </div>

        <div class="progress">
            <div class="progress-fill"
                 style="
                    width:{st.session_state.water}%;
                    background:#8fb8ba;
                 ">
            </div>
        </div>

        <div class="mini-status">
            🧹 청결　{st.session_state.clean}/100
        </div>

        <div class="progress">
            <div class="progress-fill"
                 style="
                    width:{st.session_state.clean}%;
                    background:#b5a078;
                 ">
            </div>
        </div>

        <div class="mini-status">
            💕 행복　{st.session_state.happy}/100
        </div>

        <div class="progress">
            <div class="progress-fill"
                 style="
                    width:{st.session_state.happy}%;
                    background:#d99aaa;
                 ">
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ACTION MESSAGE
# ============================================================

st.markdown(
    f"""
    <div class="notice">
        💬 {html.escape(st.session_state.message)}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ACTION BUTTONS
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#765238;
        font-size:21px;
        margin:10px 0 14px 0;
    ">
        🐹 돌봐주기
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

with col1:

    if st.button("🥬 먹이 주기"):

        st.session_state.hunger = clamp(
            st.session_state.hunger + 20
        )

        st.session_state.happy = clamp(
            st.session_state.happy + 6
        )

        st.session_state.feed_count += 1
        st.session_state.coins += 1
        st.session_state.action = "eat"

        st.session_state.message = (
            f"{st.session_state.name}가 냠냠 먹고 있어요! 🥬"
        )

        st.rerun()


with col2:

    if st.button("💧 물 채우기"):

        st.session_state.water = clamp(
            st.session_state.water + 22
        )

        st.session_state.happy = clamp(
            st.session_state.happy + 3
        )

        st.session_state.water_count += 1
        st.session_state.action = "drink"

        st.session_state.message = (
            f"{st.session_state.name}가 꼬르륵 물을 마셨어요! 💧"
        )

        st.rerun()


col3, col4 = st.columns(2)

with col3:

    if st.button("🧹 청소하기"):

        if len(st.session_state.poop) > 0:

            st.session_state.poop = []

            st.session_state.clean = 100
            st.session_state.happy = clamp(
                st.session_state.happy + 8
            )

            st.session_state.clean_count += 1
            st.session_state.coins += 2

            st.session_state.message = (
                "깨끗해졌다! ✨ 기니피그가 좋아해요!"
            )

        else:

            st.session_state.clean = 100

            st.session_state.message = (
                "이미 깨끗한 케이지예요! ✨"
            )

        st.session_state.action = "clean"

        st.rerun()


with col4:

    if st.button("🤍 쓰담쓰담"):

        st.session_state.happy = clamp(
            st.session_state.happy + 14
        )

        st.session_state.pet_count += 1
        st.session_state.coins += 1
        st.session_state.action = "pet"

        st.session_state.message = (
            f"{st.session_state.name}가 기분이 좋아졌어요! ♡"
        )

        st.rerun()


# ============================================================
# EXTRA ACTION
# ============================================================

if st.button("🌿 건초 더 채워주기"):

    st.session_state.hunger = clamp(
        st.session_state.hunger + 8
    )

    st.session_state.happy = clamp(
        st.session_state.happy + 2
    )

    st.session_state.coins += 1

    st.session_state.message = (
        "보송보송한 건초를 가득 채워줬어요! 🌿"
    )

    st.rerun()


# ============================================================
# CURRENT INFO
# ============================================================

st.markdown(
    f"""
    <div class="status-box" style="margin-top:20px;">

        <div style="
            font-size:18px;
            color:#765238;
            margin-bottom:12px;
        ">
            📖 {html.escape(st.session_state.name)}의 기록
        </div>

        <div style="
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:8px;
            color:#8d735a;
            font-size:13px;
        ">

            <div class="stat"
                 style="
                    background:#f7ecdd;
                    border-radius:12px;
                    padding:9px;
                 ">
                🥬 먹이 {st.session_state.feed_count}회
            </div>

            <div class="stat"
                 style="
                    background:#f7ecdd;
                    border-radius:12px;
                    padding:9px;
                 ">
                💧 물 {st.session_state.water_count}회
            </div>

            <div class="stat"
                 style="
                    background:#f7ecdd;
                    border-radius:12px;
                    padding:9px;
                 ">
                🧹 청소 {st.session_state.clean_count}회
            </div>

            <div class="stat"
                 style="
                    background:#f7ecdd;
                    border-radius:12px;
                    padding:9px;
                 ">
                🤍 쓰담 {st.session_state.pet_count}회
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🐹 오늘도 기니피그와 포근한 하루 ♡<br>
        작은 관심이 기니피그에게는 큰 행복이에요.
    </div>
    """,
    unsafe_allow_html=True
)
