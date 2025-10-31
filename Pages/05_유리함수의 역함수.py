import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Streamlit 페이지 설정
st.set_page_config(layout="wide")
st.title("유리함수와 역함수 디지털 교과서 📝")

# --- 함수 정의 ---
def get_plot_data(a, b, c, d, is_inverse=False, limit=10.0, resolution=800):
    """
    점근선을 기준으로 x 범위를 분할하여 수직선이 나타나지 않도록 데이터 포인트를 생성합니다.
    """
    if c == 0:
        # c=0일 경우 (일차함수 형태)는 분할이 필요 없음
        x_range = np.linspace(-limit, limit, resolution)
        if is_inverse:
            # 역함수 (y = (-dx + b) / (-a))
            y = (-d * x_range + b) / (-a) if -a != 0 else np.full_like(x_range, np.nan)
        else:
            # 원함수 (y = (ax + b) / d)
            y = (a * x_range + b) / d if d != 0 else np.full_like(x_range, np.nan)
        return [(x_range, y)]
    
    # 일반 유리함수 (c != 0)
    if is_inverse:
        # 역함수 f^-1(x): 수직 점근선 x = a/c
        asymptote = a / c
        # 역함수 함수 정의: y = (-dx + b) / (cx - a)
        func = lambda x: (-d * x + b) / (c * x - a)
    else:
        # 원함수 f(x): 수직 점근선 x = -d/c
        asymptote = -d / c
        # 원함수 함수 정의: y = (ax + b) / (cx + d)
        func = lambda x: (a * x + b) / (c * x + d)
        
    # 점근선 근처의 작은 간격 (오류 방지 영역)
    epsilon = 0.01 
    
    # 1. 왼쪽 구간: [-limit, asymptote - epsilon]
    x1 = np.linspace(-limit, asymptote - epsilon, resolution // 2)
    y1 = func(x1)
    
    # 2. 오른쪽 구간: [asymptote + epsilon, limit]
    x2 = np.linspace(asymptote + epsilon, limit, resolution // 2)
    y2 = func(x2)

    # 3. y 값이 너무 크면 nan 처리 (추가적인 안전 장치)
    y1[np.abs(y1) > 50] = np.nan
    y2[np.abs(y2) > 50] = np.nan
    
    # 두 개의 (x, y) 쌍으로 반환 (두 개의 분리된 곡선)
    return [(x1, y1), (x2, y2)]

# --- 상태 관리 및 초기값 설정 ---
# ... (이하 동일)
if 'a' not in st.session_state:
    st.session_state.a = 1
if 'b' not in st.session_state:
    st.session_state.b = 0
if 'c' not in st.session_state:
    st.session_state.c = 1
if 'd' not in st.session_state:
    st.session_state.d = 0

# --- 사이드바 (입력) ---
with st.sidebar:
    st.header("📊 계수 설정")
    
    st.write("---")
    
    # 슬라이더 (수동 설정)
    st.session_state.a = st.slider("a (분자 x 계수)", -10, 10, st.session_state.a, key='slider_a')
    st.session_state.b = st.slider("b (분자 상수항)", -10, 10, st.session_state.b, key='slider_b')
    st.session_state.c = st.slider("c (분모 x 계수)", -10, 10, st.session_state.c, key='slider_c')
    st.session_state.d = st.slider("d (분모 상수항)", -10, 10, st.session_state.d, key='slider_d')

a = st.session_state.a
b = st.session_state.b
c = st.session_state.c
d = st.session_state.d

# --- 본문 (출력) ---

# 1. 수식 (이전 코드와 동일)
st.header("1. 유리함수 및 역함수 수식")
col1, col2 = st.columns(2)
with col1:
    st.subheader("유리함수 $f(x)$")
    st.markdown(f"$$y = f(x) = \\frac{{{a}x + {b}}}{{{c}x + {d}}}$$")
with col2:
    st.subheader("역함수 $f^{-1}(x)$")
    st.markdown(f"$$y = f^{{-1}}(x) = \\frac{{{-d}x + {b}}}{{{c}x + {{-a}}}}$$")

# ---
# 2. 특이점 정보 (이전 코드와 동일)
st.header("2. 주요 정보 및 특이점")
determinant = a * d - b * c

if determinant == 0:
    st.error("🚨 **판별식 $ad-bc = 0$ 이므로, 함수가 상수가 되어 역함수가 존재하지 않습니다.** 다른 계수를 선택하세요.")
elif c == 0 and d == 0:
    st.error("🚨 **분모가 $0$ 이므로 함수가 정의되지 않습니다.** $c$ 또는 $d$ 중 하나 이상은 $0$이 아니어야 합니다.")
else:
    if a == -d:
        st.success("✅ **$a = -d$** 일 때, $f(x)$의 역함수 공식은 $f^{{-1}}(x) = \\frac{{ax + b}}{{cx + d}}$ 이 되어 **원래 함수와 식이 같습니다!**")
    
    if c != 0:
        vertical_asymptote_f = -d / c
        horizontal_asymptote_f = a / c
        st.info(f"""
        * **유리함수 $f(x)$**의 점근선: $x = {vertical_asymptote_f:.2f}$, $y = {horizontal_asymptote_f:.2f}$
        """)
    else: 
        st.warning("⚠️ **$c=0$ 이므로 함수는 일차함수 또는 상수함수 형태입니다.**")

# ---
# 3. 그래프 플롯 (수정된 데이터 생성 함수 사용)
st.header("3. 그래프 비교 (y=x 대칭 확인)")

if determinant != 0 and (c != 0 or d != 0):
    
    # get_plot_data 함수를 사용하여 데이터 포인트를 분할하여 가져옴
    data_f = get_plot_data(a, b, c, d, is_inverse=False)
    data_inv = get_plot_data(a, b, c, d, is_inverse=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 원 함수 f(x) 그리기
    for x_part, y_part in data_f:
        # 분할된 각 구간을 따로 그려 수직선 연결을 차단
        ax.plot(x_part, y_part, label=r'$f(x)$' if x_part is data_f[0][0] else None, color='blue', linestyle='-')
    
    # 역함수 f^-1(x) 그리기
    for x_part, y_part in data_inv:
        ax.plot(x_part, y_part, label=r'$f^{-1}(x)$' if x_part is data_inv[0][0] else None, color='red', linestyle='--')
    
    # y=x 직선 (대칭선)
    x_range_sym = np.linspace(-10, 10, 100)
    ax.plot(x_range_sym, x_range_sym, label=r'$y=x$', color='gray', linestyle=':', linewidth=1)
    
    # 플롯 설정
    ax.set_title("유리함수와 역함수의 그래프 (수직선 제거 완료)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    plot_limit = 10
    ax.set_xlim(-plot_limit, plot_limit)
    ax.set_ylim(-plot_limit, plot_limit)
    ax.set_aspect('equal', adjustable='box') # y=x 대칭 보장

    st.pyplot(fig)
else:
    st.warning("⚠️ **유효하지 않은 계수 조합으로 그래프를 표시할 수 없습니다.**")

# ---
# 4. 역함수 공식 유도 과정 (이전 코드와 동일)
st.header("4. 역함수 공식 유도 과정 💡")
st.markdown("유리함수의 역함수는 **$x$와 $y$의 위치를 바꾼 후** $y$에 대해 정리하여 공식 $y = \\frac{{-dx + b}}{{cx - a}}$ 를 얻게 됩니다.")

st.subheader("① 1단계: $x$와 $y$ 바꾸기")
st.markdown(f"원 함수: $$y = \\frac{{ax+b}}{{cx+d}}$$")
st.markdown(f"**$x$와 $y$를 바꾸면:** $$x = \\frac{{ay+b}}{{cy+d}}$$")

st.subheader("② 2단계: $y$에 대해 정리하기")

st.markdown(r"1. 양변에 분모를 곱하고 $y$에 관하여 정리합니다.")
st.markdown(r"$$x(cy + d) = ay + b$$")
st.markdown(r"$$cxy - ay = b - dx$$")
st.markdown(r"$$y(cx - a) = -dx + b$$")

st.markdown(r"2. **$y$에 대해 정리한 결과 (역함수):**")
st.success(r"$$y = \frac{-dx + b}{cx - a}$$")

st.markdown("---")
st.markdown("👀 **공식의 특징:** 원래 함수 $y = \\frac{{ax+b}}{{cx+d}}$ 에서 **$a$와 $d$는 자리를 바꾸면서 부호가 바뀌고**, $b$와 $c$는 그대로 유지됩니다.")
