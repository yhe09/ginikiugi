import streamlit as st
import streamlit.components.v1 as components
import random
import time


# ==============================
# 기본 설정
# ==============================

st.set_page_config(
    page_title="기니키우기",
    page_icon="🐹",
    layout="centered"
)


# ==============================
# 게임 데이터
# ==============================

if "started" not in st.session_state:
    st.session_state.started = False

if "name" not in st.session_state:
    st.session_state.name = "구구"

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

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()


# ==============================
# 시간에 따른 상태 변화
# ==============================

current_time = time.time()
passed = current_time - st.session_state.last_update

if passed >= 30:

    amount = int(passed // 30)

    st.session_state.hunger = max(
        0,
        st.session_state.hunger - amount * 2
    )

    st.session_state.water = max(
        0,
        st.session_state.water - amount * 2
    )

    st.session_state.clean = max(
        0,
        st.session_state.clean - amount
    )

    st.session_state.happy = max(
        0,
        st.session_state.happy - amount
    )

    st.session_state.last_update = current_time


# ==============================
# 전체 배경
# ==============================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7edda;
    }

    .block-container {
        max-width: 850px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==============================
# 제목
# ==============================

st.title("🐹 기니키우기")

st.caption("작고 귀여운 기니피그와 함께하는 하루")


# ==============================
# 시작 화면
# ==============================

if not st.session_state.started:

    st.subheader("🐹 새로운 친구를 만나보세요!")

    st.write("")
    st.markdown(
        """
        <div style="
            text-align:center;
            background:#fffaf0;
            border:3px solid #d8bb91;
            border-radius:25px;
            padding:30px;
            font-size:18px;
            color:#765337;
        ">
            🐹<br><br>
            먹이를 주고 🥕<br>
            물을 챙겨주고 💧<br>
            케이지를 깨끗하게 관리해주세요 🧹<br><br>
            매일매일 돌보다 보면<br>
            특별한 친구가 될 거예요!
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    new_name = st.text_input(
        "기니피그 이름",
        value="구구",
        max_chars=10
    )

    if st.button(
        "🐹 키우기 시작!",
        use_container_width=True
    ):

        if new_name.strip():
            st.session_state.name = new_name.strip()
        else:
            st.session_state.name = "구구"

        st.session_state.started = True
        st.rerun()

    st.stop()


# ==============================
# 상단 정보
# ==============================

info1, info2 = st.columns(2)

with info1:
    st.write(f"🌱 **DAY {st.session_state.day}**")

with info2:
    st.write(f"🪙 **{st.session_state.coins} 코인**")


# ==============================
# 케이지 HTML
# ==============================

name = st.session_state.name
message = st.session_state.message

poop_html = ""

for i in range(st.session_state.poop):
    positions = [
        ("25%", "72%"),
        ("38%", "80%"),
        ("55%", "75%"),
        ("70%", "82%"),
        ("82%", "70%"),
    ]

    left, bottom = positions[i % len(positions)]

    poop_html += f"""
        <div class="poop"
             style="left:{left}; bottom:{bottom};">
             💩
        </div>
    """


cage_html = f"""
<!DOCTYPE html>

<html>

<head>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    background: transparent;
}}

.cage {{
    position: relative;
    width: 100%;
    height: 500px;
    background: #fff4dc;
    border: 10px solid #b58b5d;
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 8px 0 #c49b6c;
}}


/* 바닥 */

.floor {{
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 95px;
    background: #d7b77f;
    border-top: 5px solid #bd9664;
}}


/* 철창 */

.bar {{
    position: absolute;
    top: 0;
    bottom: 90px;
    width: 5px;
    background: rgba(145,112,76,0.25);
}}

.bar1 {{ left: 12%; }}
.bar2 {{ left: 27%; }}
.bar3 {{ left: 42%; }}
.bar4 {{ left: 57%; }}
.bar5 {{ left: 72%; }}
.bar6 {{ left: 87%; }}


.horizontal {{
    position: absolute;
    left: 0;
    right: 0;
    height: 5px;
    background: rgba(145,112,76,0.18);
}}

.horizontal1 {{ top: 25%; }}
.horizontal2 {{ top: 50%; }}
.horizontal3 {{ top: 75%; }}


/* 집 */

.house {{
    position: absolute;
    left: 45px;
    bottom: 60px;
    width: 155px;
    height: 105px;
    background: #d7a66c;
    border: 5px solid #a97848;
    border-radius: 10px;
    z-index: 3;
}}

.roof {{
    position: absolute;
    left: -18px;
    top: -55px;
    width: 0;
    height: 0;
    border-left: 90px solid transparent;
    border-right: 90px solid transparent;
    border-bottom: 65px solid #a97848;
}}

.door {{
    position: absolute;
    left: 53px;
    bottom: 0;
    width: 45px;
    height: 60px;
    background: #795337;
    border-radius: 25px 25px 0 0;
}}


/* 물병 */

.water {{
    position: absolute;
    right: 55px;
    top: 60px;
    width: 45px;
    height: 105px;
    background: #bde0df;
    border: 4px solid #78aaa8;
    border-radius: 14px;
    z-index: 4;
}}

.water-cap {{
    position: absolute;
    top: -17px;
    left: 9px;
    width: 20px;
    height: 18px;
    background: #78aaa8;
    border-radius: 5px;
}}

.nozzle {{
    position: absolute;
    left: 11px;
    bottom: -35px;
    width: 20px;
    height: 40px;
    border: 5px solid #78aaa8;
    border-top: none;
    border-radius: 0 0 15px 15px;
}}


/* 밥그릇 */

.bowl {{
    position: absolute;
    right: 150px;
    bottom: 70px;
    width: 80px;
    height: 38px;
    background: #d98f72;
    border: 4px solid #a96750;
    border-radius: 0 0 40px 40px;
    z-index: 4;
}}

.food {{
    position: absolute;
    width: 12px;
    height: 12px;
    background: #9d7045;
    border-radius: 50%;
}}

.food1 {{ left: 15px; top: 7px; }}
.food2 {{ left: 34px; top: 4px; }}
.food3 {{ left: 53px; top: 8px; }}


/* 건초 */

.hay {{
    position: absolute;
    right: 25px;
    bottom: 65px;
    width: 85px;
    height: 55px;
    background: #e4bd67;
    border: 4px solid #c59b4d;
    border-radius: 15px;
    z-index: 3;
}}

.hay::after {{
    content: "🌾";
    position: absolute;
    left: 19px;
    top: 5px;
    font-size: 32px;
}}


/* 기니피그 */

.guinea {{
    position: absolute;
    left: 43%;
    bottom: 65px;
    width: 135px;
    height: 100px;
    z-index: 8;
    animation: move 3s ease-in-out infinite;
}}

.body {{
    position: absolute;
    left: 5px;
    top: 20px;
    width: 115px;
    height: 72px;
    background: #c98d60;
    border: 4px solid #8f6043;
    border-radius: 50%;
}}

.face {{
    position: absolute;
    right: 0;
    top: 10px;
    width: 68px;
    height: 68px;
    background: #dca578;
    border: 4px solid #8f6043;
    border-radius: 50%;
}}

.ear {{
    position: absolute;
    top: -5px;
    width: 24px;
    height: 24px;
    background: #d18473;
    border: 3px solid #8f6043;
    border-radius: 50%;
}}

.ear1 {{ right: 35px; }}
.ear2 {{ right: 3px; }}

.eye {{
    position: absolute;
    top: 28px;
    width: 8px;
    height: 8px;
    background: #49352a;
    border-radius: 50%;
}}

.eye1 {{ right: 38px; }}
.eye2 {{ right: 13px; }}

.nose {{
    position: absolute;
    right: -3px;
    top: 42px;
    width: 11px;
    height: 9px;
    background: #8b554d;
    border-radius: 50%;
}}

.foot {{
    position: absolute;
    bottom: -3px;
    width: 30px;
    height: 16px;
    background: #b77854;
    border: 3px solid #8f6043;
    border-radius: 50%;
}}

.foot1 {{ left: 22px; }}
.foot2 {{ left: 77px; }}


/* 움직임 */

@keyframes move {{

    0% {{
        transform: translateX(-25px) translateY(0);
    }}

    50% {{
        transform: translateX(25px) translateY(-7px);
    }}

    100% {{
        transform: translateX(-25px) translateY(0);
    }}

}}


/* 말풍선 */

.speech {{
    position: absolute;
    left: 38%;
    top: 25px;
    background: white;
    border: 3px solid #d6b88c;
    border-radius: 20px;
    padding: 10px 18px;
    color: #70563e;
    font-size: 15px;
    font-weight: bold;
    z-index: 20;
}}

.speech::after {{
    content: "";
    position: absolute;
    left: 30px;
    bottom: -12px;
    width: 18px;
    height: 18px;
    background: white;
    border-right: 3px solid #d6b88c;
    border-bottom: 3px solid #d6b88c;
    transform: rotate(45deg);
}}


/* 똥 */

.poop {{
    position: absolute;
    font-size: 20px;
    z-index: 7;
}}

</style>

</head>


<body>

<div class="cage">

    <div class="bar bar1"></div>
    <div class="bar bar2"></div>
    <div class="bar bar3"></div>
    <div class="bar bar4"></div>
    <div class="bar bar5"></div>
    <div class="bar bar6"></div>

    <div class="horizontal horizontal1"></div>
    <div class="horizontal horizontal2"></div>
    <div class="horizontal horizontal3"></div>

    <div class="floor"></div>


    <div class="house">
        <div class="roof"></div>
        <div class="door"></div>
    </div>


    <div class="water">
        <div class="water-cap"></div>
        <div class="nozzle"></div>
    </div>


    <div class="bowl">
        <div class="food food1"></div>
        <div class="food food2"></div>
        <div class="food food3"></div>
    </div>


    <div class="hay"></div>


    <div class="guinea">

        <div class="body"></div>

        <div class="face">

            <div class="ear ear1"></div>
            <div class="ear ear2"></div>

            <div class="eye eye1"></div>
            <div class="eye eye2"></div>

            <div class="nose"></div>

        </div>

        <div class="foot foot1"></div>
        <div class="foot foot2"></div>

    </div>


    <div class="speech">
        {message}
    </div>


    {poop_html}

</div>

</body>

</html>
"""


# ==============================
# 케이지 표시
# ==============================

components.html(
    cage_html,
    height=520,
    scrolling=False
)


# ==============================
# 상태
# ==============================

st.subheader(f"🐹 {st.session_state.name}의 상태")


col1, col2 = st.columns(2)

with col1:

    st.write("🥕 배고픔")
    st.progress(st.session_state.hunger)

    st.write("💧 목마름")
    st.progress(st.session_state.water)

with col2:

    st.write("🧹 깨끗함")
    st.progress(st.session_state.clean)

    st.write("💕 행복도")
    st.progress(st.session_state.happy)


st.write(f"💩 똥: {st.session_state.poop}개")


# ==============================
# 행동 버튼
# ==============================

st.subheader("🐹 돌보기")


col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "🥕 먹이 주기",
        use_container_width=True
    ):

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

    if st.button(
        "💧 물 주기",
        use_container_width=True
    ):

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

    if st.button(
        "💕 쓰다듬기",
        use_container_width=True
    ):

        st.session_state.happy = min(
            100,
            st.session_state.happy + 15
        )

        st.session_state.coins += 1

        st.session_state.message = random.choice([
            "기분 좋아! 💕",
            "헤헤 ☺️",
            "더 쓰다듬어줘!",
            "폭신폭신하지? 🐹"
        ])

        st.rerun()


col4, col5, col6 = st.columns(3)

with col4:

    if st.button(
        "🧹 똥 치우기",
        use_container_width=True
    ):

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

            st.session_state.coins += 2

            st.session_state.message = "깨끗해졌다! ✨"

        else:

            st.session_state.message = "치울 똥이 없어! 😆"

        st.rerun()


with col5:

    if st.button(
        "🌾 건초 주기",
        use_container_width=True
    ):

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

    if st.button(
        "😴 쉬기",
        use_container_width=True
    ):

        st.session_state.message = "zzz... 😴"

        st.rerun()


# ==============================
# 똥 생성
# ==============================

if random.random() < 0.03:

    if st.session_state.poop < 5:
        st.session_state.poop += 1


# ==============================
# 안내
# ==============================

st.caption(
    "💡 시간이 지나면 배고픔·목마름·청결도·행복도가 조금씩 내려가요."
)
