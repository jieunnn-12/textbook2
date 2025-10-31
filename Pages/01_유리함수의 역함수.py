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
    점근선 주변의 극단적인 값을 Mask 처리하여 그래프의 수직선 발생을 방지합니다.
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
    
    # 1. 분모가 0에 가까운 지점은 np.nan으로 처리 (분모가 0이면 함수 미정의)
    is_singular = np.abs(denominator) < 1e-6 
    y = np.where(is_singular, np.nan, numerator / denominator)
    
    # 2. 너무 큰 값(점근선 근처)도 np.nan으로 처리하여 Matplotlib이 수직선을 그리지 않도록 방지
    y = np.where(np.abs(y) > 50, np.nan, y) 
    
    return y

# --- 상태 관리 및 초기값 설정 (생략: 이전 코드와 동일) ---
if 'a' not in st.session_state:
    st.session_state.a = 1
if 'b' not in st.session_state:
    st.session_state.b = 0
if 'c' not in st.session_state:
    st.session_state.c = 1
if 'd' not in st.session_state:
    st.session_state.d = 0

def set_random_params():
    """a, b, c, d를 -10부터 10 사이의 랜덤 정수로 설정 (특이점 방지)"""
    while True:
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        d = random.randint(-10, 10)
        
        if (c != 0 or d != 0) and (a*d - b*c != 0):
            st.session_state.a = a
            st.session_state.b = b
            st.session_state.c = c
            st.session_state.d = d
            break

# --- 사이드바 (입력) ---
with st.sidebar:
    st.header("📊 계수 설정")
    st.button("랜덤 계수 생성", on_click=set_random_params)
    st.write("---")
    
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
    st.markdown(f"$$y = f^{{-1}}(x) = \\frac{{{-d}x + {b}}}{{{c}x + {{-a}}}}$$")

# --- 그래프 플롯 (생략: 이전 코드와 동일) ---
st.header("2. 그래프 비교 (y=x 대칭 확인)")

determinant = a * d - b * c

if determinant != 0 and (c != 0 or d != 0):
    
    x_range = np.linspace(-10, 10, 800) 
    y_f = calculate_function_values(x_range, a, b, c, d, is_inverse=False)
    y_inv = calculate_function_values(x_range, a, b, c, d, is_inverse=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.plot(x_range, y_f, label=r'$f(x)$', color='blue', linestyle='-')
    ax.plot(x_range, y_inv, label=r'$f^{-1}(x)$', color='red', linestyle='--')
    ax.plot(x_range, x_range, label=r'$y=x$', color='gray', linestyle=':', linewidth=1)

    ax.set_title("유리함수와 역함수의 그래프")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    plot_limit = 10
    ax.set_xlim(-plot_limit, plot_limit)
    ax.set_ylim(-plot_limit, plot_limit)
    ax.set_aspect('equal', adjustable='box') 

    st.pyplot(fig)
else:
    st.warning("⚠️ **유효하지 않은 계수 조합으로 그래프를 표시할 수 없습니다.** $ad-bc=0$ 또는 $c=0, d=0$ 인지 확인하세요.")


# --- 역함수 유도 과정 추가 (요청 반영) ---
st.header("4. 역함수 공식 유도 과정 💡")
st.markdown("유리함수의 역함수는 **$x$와 $y$의 위치를 바꾼 후** $y$에 대해 정리하여 구할 수 있습니다.")

st.subheader("① 1단계: $x$와 $y$ 바꾸기")
st.markdown(f"원 함수: $$y = \\frac{{{a}x + {b}}}{{{c}x + {d}}}$$")
st.markdown(f"**$x$와 $y$를 바꾸면:** $$x = \\frac{{{a}y + {b}}}{{{c}y + {d}}}$$")

st.subheader("② 2단계: $y$에 대해 정리하기")

st.markdown(r"1. 양변에 분모를 곱합니다.")
st.markdown(r"$$x(cy + d) = ay + b$$")

st.markdown(r"2. $y$ 항을 모으기 위해 전개합니다.")
st.markdown(r"$$cxy + dx = ay + b$$")

st.markdown(r"3. $y$를 포함하는 항을 좌변으로, 나머지를 우변으로 이항합니다.")
st.markdown(r"$$cxy - ay = b - dx$$")

st.markdown(r"4. 좌변을 $y$로 묶습니다.")
st.markdown(r"$$y(cx - a) = -dx + b$$")

st.markdown(r"5. $y$에 대해 정리합니다.")
st.markdown(r"$$y = \frac{-dx + b}{cx - a}$$")

st.subheader("③ 결론")
st.success(f"따라서 유리함수 $f(x) = \\frac{{ax+b}}{{cx+d}}$ 의 역함수는 공식 $f^{{-1}}(x) = \\frac{{-dx+b}}{{cx-a}}$ 로 구할 수 있습니다.")

st.markdown("---")
st.markdown("💡 **$a$와 $d$는 자리를 바꾸면서 부호가 바뀌고, $b$와 $c$는 자리는 그대로 부호도 그대로 유지된다는 것을 기억하세요.**")
