import streamlit as st
import random
import time
import html


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="기니키우기",
    page_icon="🐹",
    layout="centered"
)


# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;600;700&display=swap');

.stApp {
    background: #f7edda;
    color: #5c4633;
}

.block-container {
    max-width: 850px;
    padding-top: 35px;
    padding-bottom: 50px;
}

* {
    font-family: 'Noto Sans KR', sans-serif;
}

h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
}


/* 제목 */
.game-title {
    text-align: center;
    font-family: 'Jua', sans-serif;
    font-size: 48px;
    color: #765337;
    margin-bottom: 4px;
}

.game-subtitle {
    text-align: center;
    color: #a48768;
    font-size: 15px;
    margin-bottom: 25px;
}


/* 상단 정보 */
.info-box {
    background: #fffaf0;
    border: 3px solid #d8bb91;
    border-radius: 22px;
    padding: 15px 25px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    box-shadow: 0 5px 0 #c9a879;
}

.info-item {
    color: #795b3e;
    font-weight: 700;
}


/* 케이지 */
.cage {
    position: relative;
    width: 100%;
    height: 480px;
    background: #e9d0a6;
    border: 10px solid #b58b5d;
    border-radius: 30px;
    box-shadow: 0 8px 0 #c49b6c;
    overflow: hidden;
}


/* 케이지 안쪽 */
.cage-inner {
    position: absolute;
    left: 12px;
    right: 12px;
    top: 12px;
    bottom: 12px;
    background: #fff4dc;
    border-radius: 20px;
    overflow: hidden;
}


/* 철창 세로 */
.bar {
    position: absolute;
    top: 0;
    bottom: 90px;
    width: 5px;
    background: rgba(145, 112, 76, 0.28);
}

.bar1 { left: 13%; }
.bar2 { left: 29%; }
.bar3 { left: 45%; }
.bar4 { left: 61%; }
.bar5 { left: 77%; }
.bar6 { left: 93%; }


/* 철창 가로 */
.horizontal-bar {
    position: absolute;
    left: 0;
    right: 0;
    height: 5px;
    background: rgba(145, 112, 76, 0.22);
}

.horizontal1 { top: 25%; }
.horizontal2 { top: 50%; }
.horizontal3 { top: 75%; }


/* 바닥 */
.floor {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 95px;
    background: #d7b77f;
    border-top: 5px solid #bd9664;
}


/* 나무집 */
.house {
    position: absolute;
    left: 55px;
    bottom: 63px;
    width: 150px;
    height: 105px;
    background: #d7a66c;
    border: 5px solid #a97848;
    border-radius: 10px;
    z-index: 3;
}

.house-roof {
    position: absolute;
    left: -15px;
    top: -55px;
    width: 0;
    height: 0;
    border-left: 90px solid transparent;
    border-right: 90px solid transparent;
    border-bottom: 65px solid #a97848;
}

.house-door {
    position: absolute;
    bottom: 0;
    left: 52px;
    width: 45px;
    height: 62px;
    background: #795337;
    border-radius: 25px 25px 0 0;
}


/* 물병 */
.water-bottle {
    position: absolute;
    right: 45px;
    top: 65px;
    width: 45px;
    height: 105px;
    background: #bde0df;
    border: 4px solid #78aaa8;
    border-radius: 15px;
    z-index: 4;
}

.water-cap {
    position: absolute;
    top: -15px;
    left: 10px;
    width: 20px;
    height: 18px;
    background: #78aaa8;
    border-radius: 5px;
}

.water-nozzle {
    position: absolute;
    bottom: -35px;
    left: 12px;
    width: 20px;
    height: 40px;
    border: 5px solid #78aaa8;
    border-top: none;
    border-radius: 0 0 15px 15px;
}


/* 밥그릇 */
.food-bowl {
    position: absolute;
    right: 155px;
    bottom: 78px;
    width: 80px;
    height: 35px;
    background: #d98f72;
    border: 4px solid #a96750;
    border-radius: 0 0 40px 40px;
    z-index: 4;
}

.food {
    position: absolute;
    width: 13px;
    height: 13px;
    background: #9d7045;
    border-radius: 50%;
}

.food1 { left: 15px; top: 5px; }
.food2 { left: 32px; top: 2px; }
.food3 { left: 50px; top: 7px; }


/* 건초 */
.hay {
    position: absolute;
    right: 25px;
    bottom: 70px;
    width: 85px;
    height: 55px;
    background: #e4bd67;
    border-radius: 15px;
    border: 4px solid #c59b4d;
    z-index: 3;
}

.hay::before {
    content: "🌾";
    font-size: 35px;
    position: absolute;
    left: 20px;
    top: 4px;
}


/* 기니피그 */
.guinea {
    position: absolute;
    left: 45%;
    bottom: 72px;
    width: 125px;
    height: 90px;
    z-index: 6;
    animation: bounce 1.8s ease-in-out infinite;
}

.guinea-body {
    position: absolute;
    width: 110px;
    height: 72px;
    left: 8px;
    top: 15px;
    background: #c98d60;
    border-radius: 50%;
    border: 4px solid #8f6043;
}

.guinea-face {
    position: absolute;
    width: 62px;
    height: 62px;
    right: 0;
    top: 8px;
    background: #dca578;
    border-radius: 50%;
    border: 4px solid #8f6043;
}

.ear {
    position: absolute;
    width: 22px;
    height: 22px;
    background: #d18473;
    border: 3px solid #8f6043;
    border-radius: 50%;
    top: 2px;
}

.ear1 { right: 35px; }
.ear2 { right: 3px; }

.eye {
    position: absolute;
    width: 8px;
    height: 8px;
    background: #49352a;
    border-radius: 50%;
    top: 28px;
}

.eye1 { right: 38px; }
.eye2 { right: 13px; }

.nose {
    position: absolute;
    right: 0px;
    top: 40px;
    width: 10px;
    height: 8px;
    background: #8b554d;
    border-radius: 50%;
}

.mouth {
    position: absolute;
    right: 4px;
    top: 50px;
    width: 10px;
    height: 5px;
    border-bottom: 2px solid #70483d;
    border-radius: 50%;
}

.foot {
    position: absolute;
    bottom: -5px;
    width: 28px;
    height: 15px;
    background: #b77854;
    border-radius: 50%;
    border: 3px solid #8f6043;
}

.foot1 { left: 25px; }
.foot2 { left: 75px; }


@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-7px);
    }
}


/* 말풍선 */
.speech {
    position: absolute;
    left: 40%;
    top: 35px;
    background: white;
    border: 3px solid #d6b88c;
    border-radius: 20px;
    padding: 10px 18px;
    color: #70563e;
    font-weight: 600;
    z-index: 10;
}

.speech::after {
    content: "";
    position: absolute;
    bottom: -12px;
    left: 35px;
    width: 18px;
    height: 18px;
    background: white;
    border-right: 3px solid #d6b88c;
    border-bottom: 3px solid #d6b88c;
    transform: rotate(45deg);
}


/* 상태 */
.status-box {
    margin-top: 25px;
    background: #fffaf0;
    border: 3px solid #d8bb91;
    border-radius: 22px;
    padding: 20px 25px;
    box-shadow: 0 5px 0 #c9a879;
}

.status-title {
    font-family: 'Jua', sans-serif;
    font-size: 24px;
    color: #765337;
    margin-bottom: 15px;
}

.status-name {
    font-size: 18px;
    font-weight: 700;
    color: #795b3e;
    margin-bottom: 12px;
}


/* 버튼 */
.stButton > button {
    background: #fffaf0;
    color: #70563e;
    border: 3px solid #d2b387;
    border-radius: 16px;
    font-weight: 700;
    min-height: 50px;
    transition: 0.15s;
}

.stButton > button:hover {
    background: #f4e1c0;
    border-color: #b99162;
    transform: translateY(-2px);
}


/* 시작 화면 */
.start-card {
    background: #fffaf0;
    border: 4px solid #d8bb91;
    border-radius: 30px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 7px 0 #c9a879;
    margin-top: 30px;
}

.big-guinea {
    font-size: 90px;
    margin: 10px;
}

.start-text {
    color: #8a6a4b;
    line-height: 1.8;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# 세션 상태
# -----------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "guinea_name" not in st.session_state:
    st.session_state.guinea_name = "구구"

if "hunger" not in st.session_state:
    st.session_state.hunger = 80

if "water" not in st.session_state:
    st.session_state.water = 80

if "clean" not in st.session_state:
    st.session_state.clean = 90

if "happy" not in st.session_state:
    st.session_state.happy = 80

if "poop" not in st.session_state:
    st.session_state.poop = 0

if "coins" not in st.session_state:
    st.session_state.coins = 30

if "day" not in st.session_state:
    st.session_state.day = 1

if "message" not in st.session_state:
    st.session_state.message = "안녕! 🐹"

if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()


# -----------------------------
# 시간에 따른 상태 변화
# -----------------------------
now = time.time()
elapsed = now - st.session_state.last_time

if elapsed > 30:
    decrease = int(elapsed // 30)

    st.session_state.hunger = max(
        0,
        st.session_state.hunger - decrease * 2
    )

    st.session_state.water = max(
        0,
        st.session_state.water - decrease * 2
    )

    st.session_state.clean = max(
        0,
        st.session_state.clean - decrease
    )

    st.session_state.happy = max(
        0,
        st.session_state.happy - decrease
    )

    st.session_state.last_time = now


# -----------------------------
# 제목
# -----------------------------
st.markdown(
    '<div class="game-title">🐹 기니키우기</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">작고 귀여운 기니피그와 함께하는 하루</div>',
    unsafe_allow_html=True
)


# -----------------------------
# 시작 화면
# -----------------------------
if not st.session_state.started:

    st.markdown("""
    <div class="start-card">
        <div class="big-guinea">🐹</div>
        <h2>기니피그를 키워볼까요?</h2>
        <div class="start-text">
            먹이를 주고 💕<br>
            물도 챙겨주고 💧<br>
            케이지도 깨끗하게 관리해주세요 🧹<br>
            <br>
            매일매일 돌보다 보면<br>
            어느새 특별한 친구가 되어 있을 거예요!
        </div>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(
        "기니피그 이름",
        value="구구",
        max_chars=10
    )

    if st.button("🐹 키우기 시작!", use_container_width=True):

        if name.strip():
            st.session_state.guinea_name = name.strip()
        else:
            st.session_state.guinea_name = "구구"

        st.session_state.started = True
        st.rerun()

    st.stop()


# -----------------------------
# 상단 정보
# -----------------------------
safe_name = html.escape(st.session_state.guinea_name)

st.markdown(f"""
<div class="info-box">
    <div class="info-item">🌱 DAY {st.session_state.day}</div>
    <div class="info-item">🪙 {st.session_state.coins}</div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# 케이지
# -----------------------------
speech = html.escape(st.session_state.message)

cage_html = f"""
<div class="cage">

    <div class="cage-inner">

        <div class="bar bar1"></div>
        <div class="bar bar2"></div>
        <div class="bar bar3"></div>
        <div class="bar bar4"></div>
        <div class="bar bar5"></div>
        <div class="bar bar6"></div>

        <div class="horizontal-bar horizontal1"></div>
        <div class="horizontal-bar horizontal2"></div>
        <div class="horizontal-bar horizontal3"></div>

        <div class="floor"></div>

        <div class="house">
            <div class="house-roof"></div>
            <div class="house-door"></div>
        </div>

        <div class="water-bottle">
            <div class="water-cap"></div>
            <div class="water-nozzle"></div>
        </div>

        <div class="food-bowl">
            <div class="food food1"></div>
            <div class="food food2"></div>
            <div class="food food3"></div>
        </div>

        <div class="hay"></div>

        <div class="guinea">

            <div class="guinea-body"></div>

            <div class="guinea-face">
                <div class="ear ear1"></div>
                <div class="ear ear2"></div>

                <div class="eye eye1"></div>
                <div class="eye eye2"></div>

                <div class="nose"></div>
                <div class="mouth"></div>
            </div>

            <div class="foot foot1"></div>
            <div class="foot foot2"></div>

        </div>

        <div class="speech">
            {speech}
        </div>

    </div>

</div>
"""

st.markdown(cage_html, unsafe_allow_html=True)


# -----------------------------
# 상태 계산
# -----------------------------
def status_bar(value):
    value = max(0, min(100, int(value)))

    return f"""
    <div style="
        background:#eadbc3;
        border-radius:20px;
        height:18px;
        overflow:hidden;
        margin-bottom:12px;
    ">
        <div style="
            width:{value}%;
            height:100%;
            background:#c49a68;
            border-radius:20px;
        "></div>
    </div>
    """


# -----------------------------
# 상태창
# -----------------------------
st.markdown(f"""
<div class="status-box">

    <div class="status-title">🐹 {safe_name}의 상태</div>

    <div class="status-name">
        🍎 배고픔
    </div>
    {status_bar(st.session_state.hunger)}

    <div class="status-name">
        💧 목마름
    </div>
    {status_bar(st.session_state.water)}

    <div class="status-name">
        🧹 깨끗함
    </div>
    {status_bar(st.session_state.clean)}

    <div class="status-name">
        💕 행복도
    </div>
    {status_bar(st.session_state.happy)}

    <div style="margin-top:12px; color:#8a6a4b;">
        💩 현재 똥: {st.session_state.poop}개
    </div>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# 행동 버튼
# -----------------------------
st.markdown("### 🐹 돌보기")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🥕 먹이 주기", use_container_width=True):

        st.session_state.hunger = min(
            100,
            st.session_state.hunger + 20
        )

        st.session_state.happy = min(
            100,
            st.session_state.happy + 5
        )

        st.session_state.coins += 1
        st.session_state.message = "냠냠! 맛있다! 🥕"

        st.rerun()


with col2:
    if st.button("💧 물 주기", use_container_width=True):

        st.session_state.water = min(
            100,
            st.session_state.water + 25
        )

        st.session_state.happy = min(
            100,
            st.session_state.happy + 3
        )

        st.session_state.message = "꿀꺽꿀꺽 💧"

        st.rerun()


with col3:
    if st.button("💕 쓰다듬기", use_container_width=True):

        st.session_state.happy = min(
            100,
            st.session_state.happy + 15
        )

        st.session_state.message = random.choice([
            "기분 좋아! 💕",
            "헤헤 ☺️",
            "더 쓰다듬어줘!",
            "폭신폭신하지? 🐹"
        ])

        st.session_state.coins += 1

        st.rerun()


col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🧹 똥 치우기", use_container_width=True):

        if st.session_state.poop > 0:

            st.session_state.poop = 0

            st.session_state.clean = min(
                100,
                st.session_state.clean + 25
            )

            st.session_state.happy = min(
                100,
                st.session_state.happy + 5
            )

            st.session_state.message = "깨끗해졌다! ✨"

            st.session_state.coins += 2

        else:
            st.session_state.message = "치울 똥이 없어! 😆"

        st.rerun()


with col5:
    if st.button("🌾 건초 주기", use_container_width=True):

        st.session_state.hunger = min(
            100,
            st.session_state.hunger + 10
        )

        st.session_state.happy = min(
            100,
            st.session_state.happy + 4
        )

        st.session_state.message = "건초도 냠냠 🌾"

        st.rerun()


with col6:
    if st.button("😴 쉬기", use_container_width=True):

        st.session_state.message = "zzz... 😴"

        st.rerun()


# -----------------------------
# 안내
# -----------------------------
st.markdown("""
<div style="
    text-align:center;
    color:#a48768;
    margin-top:25px;
    font-size:13px;
">
    💡 시간이 지나면 배고픔·목마름·청결도가 조금씩 내려가요.
</div>
""", unsafe_allow_html=True)
