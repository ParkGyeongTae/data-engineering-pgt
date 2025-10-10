"""
uv run streamlit run stock_analysis/20251010_종목별시가총액/KOSPI_오늘기준_시가총액_상위30개_streamlit.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import pandas as pd
import streamlit as st

st.set_page_config(page_title="KOSPI 시가총액 상위 30개", layout="wide")
st.title("📊 KOSPI 시가총액 상위 30개")
df = pd.read_csv(
    "stock_analysis/20251010_종목별시가총액/KOSPI_오늘기준_시가총액_상위30개_20251010.csv",
)

# 1순위 테마별로 색상 매핑
unique_themes = df["1순위테마"].unique()
colors = st.color_picker("색상 팔레트", value="#1f77b4", key="color_picker")


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
styled_df = df.style.apply(highlight_theme, axis=1)

# 숫자 형식 지정 (소수점 셋째 자리까지만 표시)
styled_df = styled_df.format({"시가총액(조)": "{:.2f}", "시가총액비율(%)": "{:.2f}"})

st.dataframe(styled_df, use_container_width=True, height=1200)
