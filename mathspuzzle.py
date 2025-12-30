import streamlit as st
import random

# පිටුවේ සැකසුම්
st.set_page_config(page_title="ගණිත ප්‍රහේලිකා 50", page_icon="🧩", layout="centered")

# CSS මගින් පෙනුම ලස්සන කිරීම
st.markdown("""
    <style>
    .stApp { background-color: #fdfcfb; }
    .puzzle-box {
        background: white; padding: 40px; border-radius: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 6px dashed #ff9f43; text-align: center;
        margin-bottom: 20px;
    }
    .q-text { font-size: 70px !important; font-weight: bold; color: #2c3e50; }
    .stButton > button {
        height: 80px !important; font-size: 30px !important;
        font-weight: bold !important; border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ප්‍රශ්න සාදන Function එක
def create_puzzle():
    n1 = random.randint(1, 15)
    n2 = random.randint(1, 15)
    op = random.choice(['+', '-'])
    if op == '-':
        if n1 < n2: n1, n2 = n2, n1
        ans = n1 - n2
    else:
        ans = n1 + n2
    
    # පිළිතුරු හතරක් සෑදීම
    wrong = random.sample([i for i in range(0, 31) if i != ans], 3)
    options = wrong + [ans]
    random.shuffle(options)
    return {"q": f"{n1} {op} {n2}", "ans": str(ans), "options": options}

# Session State ආරම්භ කිරීම
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
    st.session_state.score = 0
    st.session_state.current_puzzle = create_puzzle()
    st.session_state.game_over = False

st.title("🧩 ගණිත ප්‍රහේලිකා අභියෝගය")

if not st.session_state.game_over:
    # Progress සහ ලකුණු
    st.write(f"### ප්‍රශ්නය: {st.session_state.q_idx + 1} / 50")
    st.progress((st.session_state.q_idx + 1) / 50)
    
    # ප්‍රශ්නය පෙන්වන කොටුව
    st.markdown(f"""
        <div class="puzzle-box">
            <p style="font-size: 20px; color: #576574;">මෙම ප්‍රහේලිකාව විසඳන්න</p>
            <h1 class="q-text">{st.session_state.current_puzzle['q']} = ?</h1>
        </div>
    """, unsafe_allow_html=True)

    # පිළිතුරු බොත්තම් (Grid එකක් ලෙස)
    st.write("### නිවැරදි Puzzle කැබැල්ල තෝරන්න:")
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.current_puzzle['options']):
        with cols[i % 2]:
            if st.button(f"🧩 {opt}", key=f"puzzle_opt_{i}", use_container_width=True):
                if str(opt) == st.session_state.current_puzzle['ans']:
                    st.session_state.score += 10
                    st.toast("නියමයි! +10", icon="⭐")
                else:
                    st.toast("වැරදුනා! උත්සාහ කරන්න", icon="❌")
                
                # මීළඟ ප්‍රශ්නයට යාම
                if st.session_state.q_idx < 49:
                    st.session_state.q_idx += 1
                    st.session_state.current_puzzle = create_puzzle()
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    st.rerun()

    st.write(f"**වත්මන් ලකුණු: {st.session_state.score}**")

else:
    # Game Over Screen
    st.balloons()
    st.markdown(f"""
        <div style="text-align: center; background: white; padding: 50px; border-radius: 30px; border: 8px solid #2ecc71;">
            <h1 style="font-size: 60px;">ප්‍රහේලිකාව අවසන්!</h1>
            <p style="font-size: 30px;">ඔබේ මුළු ලකුණු සංඛ්‍යාව</p>
            <h1 style="font-size: 100px; color: #2ecc71;">{st.session_state.score} / 500</h1>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("නැවත සෙල්ලම් කරන්න"):
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.current_puzzle = create_puzzle()
        st.session_state.game_over = False
        st.rerun()
