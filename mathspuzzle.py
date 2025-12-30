import streamlit as st
import random

st.set_page_config(page_title="ගණිත ප්‍රහේලිකා ලෝකය", page_icon="🧩", layout="centered")

# CSS - පසල් කොටු සහ වර්ණ ගැන්වීම්
st.markdown("""
    <style>
    .puzzle-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        width: 300px;
        margin: auto;
    }
    .puzzle-piece {
        width: 140px;
        height: 140px;
        background-color: #dfe6e9;
        border: 4px dashed #b2bec3;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        border-radius: 15px;
    }
    .piece-active {
        background-color: #55efc4 !important;
        border: 4px solid #00b894 !important;
        color: white;
    }
    .q-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def get_puzzle_data():
    n1 = random.randint(1, 10)
    n2 = random.randint(1, 10)
    ans = n1 + n2
    wrong = random.sample([i for i in range(1, 25) if i != ans], 3)
    options = wrong + [ans]
    random.shuffle(options)
    return {"q": f"{n1} + {n2}", "ans": str(ans), "opts": options}

if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.q_idx = 0
    st.session_state.puzzle = get_puzzle_data()
    st.session_state.solved = False

st.title("🧩 රූප ප්‍රහේලිකා දඩයම")

if st.session_state.q_idx < 50:
    st.write(f"### ප්‍රශ්නය: {st.session_state.q_idx + 1} / 50")
    
    # Visual Puzzle Grid
    # නිවැරදි පිළිතුර තේරූ විට Puzzle එක පාට වේ
    solved_class = "piece-active" if st.session_state.solved else ""
    
    st.markdown(f"""
        <div class="q-box">
            <h2 style="color: #636e72;">පහත ගැටලුව විසඳා Puzzle එක සම්පූර්ණ කරන්න</h2>
            <h1 style="font-size: 80px;">{st.session_state.puzzle['q']} = ?</h1>
        </div>
        <div class="puzzle-grid">
            <div class="puzzle-piece {solved_class}">🧩</div>
            <div class="puzzle-piece {solved_class}">🧩</div>
            <div class="puzzle-piece {solved_class}">🧩</div>
            <div class="puzzle-piece {solved_class}">🧩</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.write("### නිවැරදි පිළිතුර තෝරන්න:")
    
    # පිළිතුරු බොත්තම්
    cols = st.columns(4)
    for i, opt in enumerate(st.session_state.puzzle['opts']):
        with cols[i]:
            if st.button(str(opt), key=f"puz_{i}", use_container_width=True):
                if str(opt) == st.session_state.puzzle['ans']:
                    st.session_state.solved = True
                    st.success("ප්‍රහේලිකාව විසඳුවා! නියමයි.")
                    st.session_state.score += 10
                    st.balloons()
                    # තත්පරයකට පසු මීළඟ එකට
                    import time
                    time.sleep(1)
                    st.session_state.q_idx += 1
                    st.session_state.puzzle = get_puzzle_data()
                    st.session_state.solved = False
                    st.rerun()
                else:
                    st.error("වැරදියි, නැවත බලන්න!")

    st.write(f"**මුළු ලකුණු: {st.session_state.score}**")

else:
    st.balloons()
    st.success("විශිෂ්ටයි! ඔබ ප්‍රහේලිකා 50 ම විසඳා අවසන්.")
    st.header(f"අවසන් ලකුණු: {st.session_state.score} / 500")
    if st.button("නැවත ආරම්භ කරන්න"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.rerun()
