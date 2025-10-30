# streamlit_lotto_app.py
# Lotto 번호 추천 + 최신 당첨번호 비교 (대한민국 로또 6/45)
# 실행: pip install streamlit requests beautifulsoup4
#       streamlit run streamlit_lotto_app.py

import streamlit as st
import random
import requests
import re
from typing import List, Tuple, Dict

st.set_page_config(page_title="로또 번호 추첨기", layout="centered")

st.title("🇰🇷 로또(6/45) 번호 추첨기 — Streamlit 앱")
st.markdown("원하는 세트 수만큼 1~45 사이의 숫자 6개를 추천해줍니다. 또한 최신 회차 당첨번호와 비교할 수 있습니다.")

# ------------------- 유틸리티 함수 -------------------

def generate_lotto_set() -> List[int]:
    """1~45에서 중복 없이 6개 숫자를 뽑아 정렬해서 반환"""
    nums = random.sample(range(1, 46), 6)
    nums.sort()
    return nums


def get_latest_draw_number() -> int:
    """동행복권 '회차별 당첨번호' 페이지를 스크래핑해서 최신 회차 번호를 추출합니다.
    (성공하면 정수 회차 반환, 실패하면 -1)
    """
    try:
        url = "https://m.dhlottery.co.kr/gameResult.do?method=byWin"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        text = resp.text
        # "제 1195회" 또는 "1195회" 등을 찾아 첫 번째 숫자 그룹을 회차로 사용
        m = re.search(r"(\d+)\s*회", text)
        if m:
            return int(m.group(1))
    except Exception:
        return -1
    return -1


def fetch_lotto_numbers_for_draw(draw_no: int) -> Dict:
    """공식 API를 이용해 해당 회차의 당첨번호(및 보너스 등)를 JSON으로 가져옵니다.
    반환 예시: {"drwNo": 1195, "numbers": [3,15,27,33,34,36], "bnusNo": 37, "returnValue": "success"}
    실패 시 {'returnValue': 'fail'} 를 반환
    """
    api = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={draw_no}"
    try:
        r = requests.get(api, timeout=5)
        r.raise_for_status()
        data = r.json()
        if data.get("returnValue") == "success":
            numbers = [data.get(f"drwtNo{i}") for i in range(1,7)]
            bn = data.get("bnusNo")
            return {"drwNo": data.get("drwNo"), "numbers": numbers, "bnusNo": bn, "returnValue": "success"}
    except Exception:
        pass
    return {"returnValue": "fail"}


def rank_from_match_count(match_count: int, bonus_matched: bool) -> Tuple[str, int]:
    """로또 등수 판정 (대한민국 규칙)
    return: (rank_name, rank_number) or ("낙첨", 0)
    규칙:
      6개 일치 -> 1등
      5개 + 보너스 -> 2등
      5개 -> 3등
      4개 -> 4등
      3개 -> 5등
      else -> 낙첨
    """
    if match_count == 6:
        return ("1등", 1)
    if match_count == 5 and bonus_matched:
        return ("2등", 2)
    if match_count == 5:
        return ("3등", 3)
    if match_count == 4:
        return ("4등", 4)
    if match_count == 3:
        return ("5등", 5)
    return ("낙첨", 0)

# ------------------- UI 컨트롤 -------------------

st.sidebar.header("설정")
num_sets = st.sidebar.number_input("생성할 세트 수", min_value=1, max_value=20, value=5, step=1)
seed = st.sidebar.text_input("(선택) 랜덤 시드값 — 고정된 결과가 필요하면 숫자 입력", value="")
if seed.strip():
    try:
        random.seed(int(seed))
    except Exception:
        st.sidebar.warning("시드는 정수로 입력하세요. 무시됩니다.")

st.sidebar.markdown("---")
compare_mode = st.sidebar.radio("비교 방식", ("최근 회차와 비교 (자동)", "특정 회차와 비교 (직접 입력)", "비교 안함"))
manual_draw = None
if compare_mode == "특정 회차와 비교 (직접 입력)":
    manual_draw = st.sidebar.number_input("비교할 회차 번호", min_value=1, value=1, step=1)

if st.sidebar.button("생성하기"):
    # 생성
    generated = [generate_lotto_set() for _ in range(num_sets)]

    st.subheader("생성된 번호")
    for i, s in enumerate(generated, start=1):
        st.write(f"세트 {i}: {s}")

    # 비교
    if compare_mode == "비교 안함":
        st.info("비교를 선택하지 않았습니다.")
        st.stop()

    # 최신 회차 자동 조회
    target_draw = None
    if compare_mode == "최근 회차와 비교 (자동)":
        st.info("최근 회차 정보를 불러오는 중... (동행복권 사이트에서 회차 정보를 가져옵니다)")
        latest = get_latest_draw_number()
        if latest == -1:
            st.error("최근 회차 정보를 불러오지 못했습니다. 네트워크 연결을 확인하거나 나중에 시도하세요.")
            st.stop()
        target_draw = latest
    else:
        target_draw = manual_draw

    st.write(f"비교 대상 회차: {target_draw}회")

    api_res = fetch_lotto_numbers_for_draw(target_draw)
    if api_res.get("returnValue") != "success":
        st.error("당첨번호 정보를 불러오지 못했습니다. 회차 번호가 유효한지 확인하세요.")
        st.stop()

    official = api_res["numbers"]
    bonus = api_res["bnusNo"]
    st.success(f"공식 당첨번호({target_draw}회): {official}  + 보너스: {bonus}")

    st.subheader("비교 결과")
    for i, s in enumerate(generated, start=1):
        matched = len(set(s) & set(official))
        bonus_matched = bonus in s
        rank_name, rank_num = rank_from_match_count(matched, bonus_matched)
        st.write(f"세트 {i}: {s}  → 맞춘 개수: {matched}, 보너스 일치: {bonus_matched}  → {rank_name}")

    st.info("참고: 1등~5등 판정은 대한민국 로또 규칙에 따라 수행됩니다.")
else:
    st.write("왼쪽 사이드바에서 생성할 세트 수를 선택한 뒤 '생성하기' 버튼을 눌러주세요.")

# ------------------- 추가 도움말 -------------------

st.markdown("---")
st.markdown("**구현 노트**:\n- 최신 당첨번호는 동행복권 사이트의 정보를 사용합니다.\n- 본 앱은 교육/오락용이며 당첨을 보장하지 않습니다.")
