import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Streamlit 페이지 설정
st.set_page_config(layout="wide")
st.title("유리함수와 역함수 디지털 교과서 📝")

# --- 함수 정의 ---
def rational_function(x, a, b, c, d):
    """유리함수 f(x) = (ax + b) / (cx + d)"""
    # 분모가 0이 되는 지점 처리
    if c == 0 and d == 0:
        return np.nan # 정의되지 않음
    if c != 0 and abs(x - (-d/c)) < 1e-9:
        return np.nan # 점근선
    
    numerator = a * x + b
    denominator = c * x + d
    return numerator / denominator

def inverse_rational_function(x, a, b, c, d):
    """역함수 f^(-1)(x) = (-dx + b) / (cx - a)"""
    # 분모가 0이 되는 지점 처리
    if c == 0 and a == 0:
        return np.nan # 정의되지 않음
    if c != 0 and abs(x - (a/c)) < 1e-9:
        return np.nan # 점근선
        
    numerator = -d * x + b
    denominator = c * x - a
    return numerator / denominator

# --- 상태 관리 및 초기값 설정 ---

# 세션 상태에 a, b, c, d 값 저장 (Streamlit에서 값 유지 및 업데이트를 위해 사용)
if 'a' not in st.session_state:
    st.session_state.a = 1
if 'b' not in st.session_state:
    st.session_state.b = 0
if 'c' not in st.session_state:
    st.session_state.c = 1
if 'd' not in st.session_state:
    st.session_state.d = 0

def set_random_params():
    """a, b, c, d를 -10부터 10 사이의 랜덤 정수로 설정"""
    # c와 (ad-bc)가 0이 되는 것을 방지하기 위해 최소한의 제약 추가
    while True:
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        d = random.randint(-10, 10)
        
        # c=0 이고 a=0 이거나, c=0 이고 d=0 인 경우 (역함수 또는 함수 자체가 상수가 되는 경우)
        # 또는 ad-bc=0 인 경우 (역함수가 존재하지 않거나 상수가 되는 경우)
        # 유리함수의 일반적인 형태가 나타나도록 c!=0 또는 d!=0 이고 ad-bc != 0 을 만족하는 것을 목표로 함
        if (c != 0 or d != 0) and (a*d - b*c != 0):
             # cx+d = 0, cx-a = 0 의 점근선이 너무 좁지 않도록 c, d, a 의 값 조정 (필요시)
            st.session_state.a = a
            st.session_state.b = b
            st.session_state.c = c
            st.session_state.d = d
            break

# --- 사이드바 (입력) ---
with st.sidebar:
    st.header("📊 계수 설정")
    
    # 랜덤 값 버튼
    st.button("랜덤 계수 생성", on_click=set_random_params)
    
    st.write("---")
    
    # 슬라이더를 사용하여 계수 a, b, c, d 설정
    st.session_state.a = st.slider("a (분자 x 계수)", -10, 10, st.session_state.a, key='slider_a')
    st.session_state.b = st.slider("b (분자 상수항)", -10, 10, st.session_state.b, key='slider_b')
    st.session_state.c = st.slider("c (분모 x 계수)", -10, 10, st.session_state.c, key='slider_c')
    st.session_state.d = st.slider("d (분모 상수항)", -10, 10, st.session_state.d, key='slider_d')

a = st.session_state.a
b = st.session_state.b
c = st.session_state.c
d = st.session_state.d

# --- 본문 (출력) ---

st.header("1. 유리함수 및 역함수 수식")
col1, col2 = st.columns(2)

with col1:
    st.subheader("유리함수 $f(x)$")
    st.markdown(f"$$y = f(x) = \\frac{{{a}x + {b}}}{{{c}x + {d}}}$$")
    
with col2:
    st.subheader("역함수 $f^{-1}(x)$")
    st.markdown(f"$$y = f^{{-1}}(x) = \\frac{{{-d}x + {b}}}{{{c}x - {a}}} = \\frac{{{-d}x + {b}}}{{{c}x + {{-a}}}}$$")

# --- 예외 처리 및 정보 표시 ---
st.header("2. 주요 정보 및 특이점")

determinant = a * d - b * c

if determinant == 0:
    st.error("🚨 **판별식 $ad-bc = 0$ 이므로, 함수가 상수가 되어 역함수가 존재하지 않습니다.** 다른 계수를 선택하세요.")
elif c == 0 and d == 0:
    st.error("🚨 **분모가 $0$ 이므로 함수가 정의되지 않습니다.** $c$ 또는 $d$ 중 하나 이상은 $0$이 아니어야 합니다.")
else:
    # 점근선 정보
    if c != 0:
        vertical_asymptote_f = -d / c
        horizontal_asymptote_f = a / c
        vertical_asymptote_inv = a / c
        horizontal_asymptote_inv = -d / c
        
        st.info(f"""
        * **유리함수 $f(x)$**의 점근선: $x = \\frac{{-d}}{{c}} = {vertical_asymptote_f:.2f}$, $y = \\frac{{a}}{{c}} = {horizontal_asymptote_f:.2f}$
        * **역함수 $f^{{-1}}(x)$**의 점근선: $x = \\frac{{a}}{{c}} = {vertical_asymptote_inv:.2f}$, $y = \\frac{{-d}}{{c}} = {horizontal_asymptote_inv:.2f}$
        
        **👉 $f(x)$의 수직 점근선 ($x$)이 $f^{{-1}}(x)$의 수평 점근선 ($y$)이 되고, $f(x)$의 수평 점근선 ($y$)이 $f^{{-1}}(x)$의 수직 점근선 ($x$)이 되어 $y=x$ 대칭임을 확인할 수 있습니다.**
        """)
    else: # c == 0 인 경우 (일차함수 형태)
        if a == 0:
             st.error("🚨 **$a=0, c=0$ 이면 함수가 $y=b/d$ 인 상수함수 형태입니다.** 역함수가 존재하지 않습니다.")
        else:
            st.warning("⚠️ **$c=0$ 이므로 함수는 $y = \\frac{a}{d}x + \\frac{b}{d}$ 형태의 일차함수입니다.**")


# --- 그래프 플롯 ---
st.header("3. 그래프 비교 (y=x 대칭 확인)")

if determinant != 0 and (c != 0 or d != 0):
    
    # 그래프 범위 설정
    x_range = np.linspace(-10, 10, 400)
    
    # 함수 값 계산
    y_f = np.array([rational_function(x, a, b, c, d) for x in x_range])
    y_inv = np.array([inverse_rational_function(x, a, b, c, d) for x in x_range])

    # 플롯 생성
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 1. 원 함수 f(x)
    ax.plot(x_range, y_f, label=r'$f(x) = \frac{'+str(a)+'x+'+str(b)+'}{'+str(c)+'x+'+str(d)+'}$', color='blue', linestyle='-')
    
    # 2. 역함수 f^-1(x)
    ax.plot(x_range, y_inv, label=r'$f^{-1}(x) = \frac{'+str(-d)+'x+'+str(b)+'}{'+str(c)+'x+'+str(-a)+'}$', color='red', linestyle='--')
    
    # 3. y=x 직선 (대칭선)
    ax.plot(x_range, x_range, label=r'$y=x$', color='gray', linestyle=':', linewidth=1)

    # 4. 점근선 표시
    if c != 0:
        # f(x) 점근선
        ax.axvline(vertical_asymptote_f, color='blue', linestyle=':', linewidth=0.8)
        ax.axhline(horizontal_asymptote_f, color='blue', linestyle=':', linewidth=0.8)
        # f^-1(x) 점근선
        ax.axvline(vertical_asymptote_inv, color='red', linestyle=':', linewidth=0.8)
        ax.axhline(horizontal_asymptote_inv, color='red', linestyle=':', linewidth=0.8)
    
    # 플롯 설정
    ax.set_title("유리함수와 역함수의 그래프")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box') # x, y축 비율을 1:1로 설정하여 대칭 확인 용이

    st.pyplot(fig)
else:
    st.warning("⚠️ **유효하지 않은 계수 조합으로 그래프를 표시할 수 없습니다.** 위의 '주요 정보 및 특이점'을 확인하세요.")

st.markdown("---")
st.markdown("💡 **유리함수 $f(x)$와 역함수 $f^{-1}(x)$의 그래프가 $y=x$ 직선에 대하여 서로 대칭인지 확인해 보세요.**")

