"""
uv run streamlit run stock_analysis/20251010_종목별시가총액/KOSPI_테마별_시가총액_분석_streamlit.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import pandas as pd
import streamlit as st

st.set_page_config(page_title="KOSPI 테마별 시가총액 분석", layout="wide")
st.title("📊 KOSPI 테마별 시가총액 분석")

# 데이터 로드
df = pd.read_csv(
    "stock_analysis/20251010_종목별시가총액/KOSPI_오늘기준_시가총액_상위50개_20251010.csv",
)

# 1순위 테마별로 그룹화하여 시가총액과 비율 집계
theme_analysis = (
    df.groupby("1순위테마")
    .agg({"시가총액(조)": "sum", "시가총액비율(%)": "sum", "종목명": "count"})
    .round(3)
)

# 컬럼명 변경
theme_analysis.columns = ["총시가총액(조)", "총시가총액비율(%)", "종목수"]
theme_analysis = theme_analysis.sort_values("총시가총액(조)", ascending=False)

# 인덱스를 컬럼으로 변환
theme_analysis = theme_analysis.reset_index()
theme_analysis.columns = ["1순위테마", "총시가총액(조)", "총시가총액비율(%)", "종목수"]

# 순위 추가
theme_analysis.insert(0, "순위", range(1, len(theme_analysis) + 1))

# 테마별 색상 매핑
unique_themes = theme_analysis["1순위테마"].unique()


def highlight_theme(row):
    """1순위 테마별로 배경색 적용"""
    theme = row["1순위테마"]
    theme_index = list(unique_themes).index(theme)

    # 테마별로 다른 색상 생성 (HSV 색상 공간 활용)
    hue = (theme_index * 137.5) % 360  # 황금각 사용
    saturation = 0.6
    lightness = 0.3  # 더 어둡게 조정

    # HSL을 RGB로 변환
    import colorsys

    r, g, b = colorsys.hls_to_rgb(hue / 360, lightness, saturation)
    bg_color = f"background-color: rgb({int(r*255)}, {int(g*255)}, {int(b*255)}); color: white;"

    return [bg_color] * len(row)


# 스타일 적용
styled_df = theme_analysis.style.apply(highlight_theme, axis=1)

# 숫자 형식 지정 (소수점 셋째 자리까지만 표시)
styled_df = styled_df.format(
    {"총시가총액(조)": "{:.3f}", "총시가총액비율(%)": "{:.3f}"}
)

# 메트릭 표시
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("총 테마 수", len(theme_analysis))
with col2:
    st.metric("총 시가총액(조)", f"{theme_analysis['총시가총액(조)'].sum():.1f}")
with col3:
    st.metric("1위 테마", theme_analysis.iloc[0]["1순위테마"])
with col4:
    st.metric("1위 테마 비율", f"{theme_analysis.iloc[0]['총시가총액비율(%)']:.1f}%")

# 테마별 분석 테이블
st.subheader("📈 테마별 시가총액 분석")
st.dataframe(styled_df, use_container_width=True, height=600)

# 상위 5개 테마 차트
st.subheader("📊 상위 5개 테마 시가총액")
top5_themes = theme_analysis.head(5)

import plotly.express as px

fig = px.bar(
    top5_themes,
    x="1순위테마",
    y="총시가총액(조)",
    title="상위 5개 테마별 시가총액",
    color="1순위테마",
    color_discrete_sequence=px.colors.qualitative.Set3,
)
fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=500)
st.plotly_chart(fig, use_container_width=True)

# 상위 5개 테마 비율 파이 차트
st.subheader("🥧 상위 5개 테마 비율")
fig_pie = px.pie(
    top5_themes,
    values="총시가총액비율(%)",
    names="1순위테마",
    title="상위 5개 테마별 시가총액 비율",
)
fig_pie.update_layout(height=500)
st.plotly_chart(fig_pie, use_container_width=True)
