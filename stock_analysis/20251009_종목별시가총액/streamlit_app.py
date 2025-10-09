"""
uv run streamlit run stock_analysis/20251009_종목별시가총액/streamlit_app.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import pandas as pd
import streamlit as st

st.title("KOSPI 시가총액 상위 100개 + 테마")
top100 = pd.read_csv("stock_analysis/20251009_종목별시가총액/KOSPI_TOP100_20251002.csv")

st.dataframe(top100, width="content")
