import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# --- Streamlit UI 구성 ---

st.title("이차함수의 그래프 기본형($y=ax^2$) 분석하기")
st.markdown("슬라이더를 움직여 $a$ 값을 바꿔보며 그래프의 모양과 폭이 어떻게 변하는지 관찰해 보세요.")

# 1. 사용자 입력 (a 값 선택)
st.sidebar.header("함수 설정")
# a 값 슬라이더. -3.0부터 3.0까지, 소수점 둘째 자리까지 선택 가능
a_value = st.sidebar.slider(
    "계수 $a$ 값 선택:", 
    min_value=-3.0, 
    max_value=3.0, 
    value=1.0, 
    step=0.1,
    format="%.1f"
)

# 비교를 위한 기본 그래프 표시 여부
show_base = st.sidebar.checkbox("비교용 기본 그래프 ($y=x^2$) 함께 표시", value=False)
st.sidebar.markdown("---")


# a=0 인 경우 경고 (이차함수가 아니므로)
if a_value == 0:
    st.warning("경고: $a$가 0이면 이차함수 $y=ax^2$가 아닌 $y=0$ (x축)이 됩니다. $a$를 0이 아닌 값으로 선택해 주세요.")
else:
    # 2. 그래프 데이터 생성
    x = np.linspace(-5, 5, 100)
    y = a_value * x**2

    # Plotly Graph Objects를 사용하여 fig 객체 생성
    fig = go.Figure()
    
    # 3. 현재 함수 그래프 추가
    fig.add_trace(go.Scatter(
        x=x, y=y, 
        mode='lines', 
        name=f'$y={a_value}x^2$', 
        line=dict(color='blue', width=3)
    ))
    
    # 4. 기본 그래프 추가 (선택 사항)
    if show_base:
        y_base = 1.0 * x**2
        fig.add_trace(go.Scatter(
            x=x, y=y_base, 
            mode='lines', 
            name='$y=x^2$ (비교)', 
            line=dict(color='gray', dash='dot', width=2)
        ))

    # 5. 그래프 레이아웃 설정
    fig.update_layout(
        title=f"이차함수 그래프: $y={a_value}x^2$",
        xaxis_title='$x$',
        yaxis_title='$y$',
        legend_title="함수",
        height=500
    )
    
    # 축 범위 고정 및 중앙에 표시
    fig.update_xaxes(range=[-5.5, 5.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
    fig.update_yaxes(range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='black')

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 6. 분석 결과 출력
    st.subheader("그래프 분석 결과")
    
    # --- 볼록성 추론 ---
    st.markdown("### 1. 볼록성 확인 (그래프의 모양)")
    if a_value > 0:
        st.success(f"현재 $a = {a_value}$ (양수)입니다. 그래프가 **아래로 볼록**임을 확인했습니다. 🧐")
        st.markdown(
            "> **귀납적 추론:** $a$가 **양수**일 때 ($a > 0$), 이차함수 $y=ax^2$의 그래프는 **아래로 볼록**입니다."
        )
    else: # a_value < 0
        st.error(f"현재 $a = {a_value}$ (음수)입니다. 그래프가 **위로 볼록**임을 확인했습니다. 🤔")
        st.markdown(
            "> **귀납적 추론:** $a$가 **음수**일 때 ($a < 0$), 이차함수 $y=ax^2$의 그래프는 **위로 볼록**입니다."
        )

    # --- 폭의 변화 추론 ---
    st.markdown("### 2. 폭의 변화 확인 ($a$의 절댓값)")
    abs_a = abs(a_value)
    st.info(f"현재 $a$의 **절댓값**은 $|a| = {abs_a}$ 입니다.")
    
    if abs_a > 1.0:
        st.markdown("> **$|a|$가 1보다 클수록** ($|a| > 1$), 그래프의 폭은 $y=x^2$ 그래프보다 **좁아집니다** (y축에 가까워집니다).")
    elif abs_a < 1.0 and abs_a != 0:
        st.markdown("> **$|a|$가 0과 1 사이일수록** ($0 < |a| < 1$), 그래프의 폭은 $y=x^2$ 그래프보다 **넓어집니다** (x축에 가까워집니다).")
    else: # abs_a == 1.0
        st.markdown("> **$|a|$가 1일 때** ($|a| = 1$), 그래프의 폭은 기본 형태인 $y=x^2$ 또는 $y=-x^2$와 같습니다.")
    
    st.markdown(
        "**최종 추론:** $a$의 절댓값 **$|a|$이 클수록** 그래프의 폭은 **좁아지고**, **$|a|$이 작을수록** 그래프의 폭은 **넓어집니다**."
    )

st.markdown("---")
st.caption("이 앱은 Plotly를 사용하여 대화형 그래프를 제공합니다. 마우스를 올려 값을 확인하고 확대/축소할 수 있습니다.")

