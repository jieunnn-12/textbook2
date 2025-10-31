import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Streamlit 페이지 설정
st.set_page_config(layout="wide")
st.title("유리함수와 역함수 디지털 교과서 📝")

# --- 함수 정의 ---
def calculate_function_values(x_range, a, b, c, d, is_inverse=False):
    """
    유리함수 또는 역함수의 값을 계산하고 
    점근선 주변의 극단적인 값을 NaN으로 처리하여 그래프의 수직선 발생을 방지합니다.
    """
    if is_inverse:
        # 역함수: y = (-dx + b) / (cx - a)
        den_x_coef = c
        den_const = -a
        num_x_coef = -d
        num_const = b
    else:
        # 원 함수: y = (ax + b) / (cx + d)
        den_x_coef = c
        den_const = d
        num_x_coef = a
        num_const = b
        
    numerator = num_x_coef * x_range + num_const
    denominator = den_x_coef * x_range + den_const
    
    # 1. 분모가 0에 가까운 지점은 np.nan으로 처리 (함수 미정의)
    is_singular = np.abs(denominator) < 1e-6 
    y = np.where(is_singular, np.nan, numerator / denominator)
    
    # 2. **수직선 제거 핵심**: y 값이 일정 범위를 벗어나는 경우 (극한값) np.nan으로 처리하여 
    # Matplotlib이 점을 연결하지 못하도록 막아 수직선이 생기는 것을 방지합니다.
    y = np.where(np.abs(y) > 50, np.nan, y) 
    
    return y

# --- 상태 관리 및 초기값 설정 ---
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

# 1. 수식
st.header("1. 유리함수 및 역함수 수식")
col1, col2 = st.columns(2)

with col1:
    st.subheader("유리함수 $f(x)$")
    st.markdown(f"$$y = f(x) = \\frac{{{a}x + {b}}}{{{c}x + {d}}}$$")
    
with col2:
    st.subheader("역함수 $f^{-1}(x)$")
    st.markdown(f"$$y = f^{{-1}}(x) = \\frac{{{-d}x + {b}}}{{{c}x + {{-a}}}}$$")

# ---
# 2. 특이점 정보
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
        
        **👉 참고:** $f(x)$의 수직 점근선 ($x$)이 $f^{{-1}}(x)$의 수평 점근선 ($y$)이 되고, $f(x)$의 수평 점근선 ($y$)이 $f^{{-1}}(x)$의 수직 점근선 ($x$)이 됩니다.
        """)
    else: 
        st.warning("⚠️ **$c=0$ 이므로 함수는 일차함수 또는 상수함수 형태입니다.**")

# ---
# 3. 그래프 플롯
st.header("3. 그래프 비교 (y=x 대칭 확인)")

if determinant != 0 and (c != 0 or d != 0):
    
    x_range = np.linspace(-10, 10, 800) 
    y_f = calculate_function_values(x_range, a, b, c, d, is_inverse=False)
    y_inv = calculate_function_values(x_range, a, b, c, d, is_inverse=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 1. 원 함수 f(x)
    ax.plot(x_range, y_f, label=r'$f(x)$', color='blue', linestyle='-')
    
    # 2. 역함수 f^-1(x)
    ax.plot(x_range, y_inv, label=r'$f^{-1}(x)$', color='red', linestyle='--')
    
    # 3. y=x 직선 (대칭선)
    ax.plot(x_range, x_range, label=r'$y=x$', color='gray', linestyle=':', linewidth=1)
    
    # 플롯 설정
    ax.set_title("유리함수와 역함수의 그래프 (수직선 제거됨)")
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
# 4. 역함수 공식 유도 과정
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
