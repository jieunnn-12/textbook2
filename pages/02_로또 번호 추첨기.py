import streamlit as st
import random

# --- 최근 로또 당첨 번호 설정 (수동 업데이트 필요) ---
RECENT_WINNING_NUMBERS = {
    '회차': '제1195회 (2025.10.25)',
    '당첨번호': [3, 15, 27, 33, 34, 36],
    '보너스번호': 37
}

def generate_lotto_numbers():
    """1부터 45까지의 숫자 중 6개를 중복 없이 무작위로 생성합니다."""
    return sorted(random.sample(range(1, 46), 6))

def compare_numbers(my_numbers, winning_numbers, bonus_number):
    """생성된 번호와 당첨 번호를 비교하여 결과를 반환합니다."""
    
    match_count = len(set(my_numbers) & set(winning_numbers))
    bonus_match = bonus_number in my_numbers
    
    if match_count == 6:
        rank = "1등"
    elif match_count == 5 and bonus_match:
        rank = "2등"
    elif match_count == 5:
        rank = "3등"
    elif match_count == 4:
        rank = "4등"
    elif match_count == 3:
        rank = "5등"
    else:
        rank = "꽝"
        
    return match_count, bonus_match, rank

# --- Streamlit UI 구성 ---

st.title("💰 로또 6/45 번호 추첨기")
st.markdown("1부터 45까지의 숫자 중에서 6개의 로또 번호를 추첨합니다.")

st.sidebar.header("설정")

# 몇 세트를 만들지 선택하는 숫자 입력
num_sets = st.sidebar.number_input(
    "추첨할 세트 수 (1~20)", 
    min_value=1, 
    max_value=20, 
    value=5, 
    step=1
)

# 생성 버튼을 누르면
if st.sidebar.button("🔢 생성 버튼"):
    # 1. 풍선 띄우기 기능 추가
    st.balloons()
    
    # 2. 결과 제목의 색상을 하늘색으로 변경
    st.markdown(
        f"<h2 style='color:skyblue;'>{num_sets} 세트 추첨 결과</h2>", 
        unsafe_allow_html=True
    )
    
    # 당첨 번호 표시
    winning_nums = RECENT_WINNING_NUMBERS['당첨번호']
    bonus_num = RECENT_WINNING_NUMBERS['보너스번호']
    st.info(
        f"**최근 당첨 번호 ({RECENT_WINNING_NUMBERS['회차']}):** "
        f"{', '.join(map(str, winning_nums))} "
        f"**+ 보너스 {bonus_num}**"
    )

    results_data = []
    
    for i in range(1, num_sets + 1):
        my_numbers = generate_lotto_numbers()
        match_count, bonus_match, rank = compare_numbers(my_numbers, winning_nums, bonus_num)

        # 등수별 색상 설정
        if rank == "1등":
            rank_color = "green"
        elif rank == "2등":
            rank_color = "darkgreen"
        elif rank == "3등":
            rank_color = "orange"
        elif rank == "4등":
            rank_color = "blue"
        elif rank == "5등":
            rank_color = "teal"
        else:
            rank_color = "grey"
        
        results_data.append({
            "세트": f"{i}번",
            "번호": ", ".join(map(str, my_numbers)),
            "일치 개수": f"{match_count}개",
            "보너스 일치": "✅" if bonus_match else "❌",
            "결과": f"<span style='color:{rank_color}; font-weight:bold;'>{rank}</span>"
        })

    # 테이블 표시 (HTML 사용)
    st.markdown(
        """
        <style>
        .dataframe th, .dataframe td {
            text-align: center !important;
            vertical-align: middle !important;
            padding: 8px 12px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    html_table = "<table>"
    html_table += "<thead><tr><th>세트</th><th>번호</th><th>일치 개수</th><th>보너스 일치</th><th>결과</th></tr></thead>"
    html_table += "<tbody>"
    for row in results_data:
        html_table += f"<tr><td>{row['세트']}</td><td>{row['번호']}</td><td>{row['일치 개수']}</td><td>{row['보너스 일치']}</td><td>{row['결과']}</td></tr>"
    html_table += "</tbody></table>"

    st.markdown(html_table, unsafe_allow_html=True)

st.markdown("---")
st.caption("참고: 로또 당첨 번호는 수동으로 업데이트해야 합니다.")
