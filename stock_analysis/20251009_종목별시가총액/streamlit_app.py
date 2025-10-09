"""
uv run streamlit run stock_analysis/20251009_종목별시가총액/streamlit_app.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="KOSPI 시가총액 3년 비교", layout="wide")
st.title("📊 KOSPI 시가총액 상위 20개 (3년 비교)")

# CSV 로드
df = pd.read_csv(
    # "stock_analysis/20251009_종목별시가총액/KOSPI_TOP10_3시점비교_요약형.csv"
    "stock_analysis/20251009_종목별시가총액/SP500_TOP20_3시점비교_요약형.csv"
)

# ✅ 인덱스 제거
df = df.reset_index(drop=True)


# ✅ 테마 추출 함수
def extract_themes(df: pd.DataFrame):
    themes = set()
    for col in df.columns:
        if "종목(테마)" in col:
            for cell in df[col].dropna():
                if "(" in cell and ")" in cell:
                    theme = cell.split("(")[-1].replace(")", "").strip()
                    themes.add(theme)
    return sorted(list(themes))


themes = extract_themes(df)

# ✅ 테마별 색상 매핑
palette = sns.color_palette("tab20", len(themes))
theme_colors = {
    theme: f"background-color: rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, 0.3)"
    for theme, (r, g, b) in zip(themes, palette)
}


# ✅ 셀별 색상 스타일 적용 함수
def highlight_theme(cell):
    if isinstance(cell, str) and "(" in cell and ")" in cell:
        theme = cell.split("(")[-1].replace(")", "").strip()
        return theme_colors.get(theme, "")
    return ""


# ✅ 스타일 적용
styled_df = df.style.applymap(highlight_theme)

st.dataframe(styled_df, use_container_width=True)
