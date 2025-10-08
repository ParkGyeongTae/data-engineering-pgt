"""
uv run python stock_analysis/main.py
"""

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pykrx")

from datetime import datetime, timedelta

import pandas as pd
from dateutil.relativedelta import relativedelta
from pykrx import stock

today = datetime.now()
_today = today.strftime("%Y%m%d")
_one_month_ago = (today - relativedelta(months=1)).strftime("%Y%m%d")
_three_months_ago = (today - relativedelta(months=3)).strftime("%Y%m%d")
_six_months_ago = (today - relativedelta(months=6)).strftime("%Y%m%d")
_one_year_ago = (today - relativedelta(years=1)).strftime("%Y%m%d")
_two_years_ago = (today - relativedelta(years=2)).strftime("%Y%m%d")

results = []

stock_codes = [
    "005930",
    # "000660",
    # "005380",
    # "005935",
    # "005930",
]

for stock_code in stock_codes:
    df_price = stock.get_market_ohlcv_by_date(_one_year_ago, _today, stock_code)
    df_price["거래대금(억)"] = (
        (df_price["거래량"] * df_price["종가"] / 1e8).round(0).astype(int)
    )
    df_price = df_price[["종가", "거래대금(억)"]]

    df_cap = stock.get_market_cap_by_date(_one_year_ago, _today, stock_code)
    df_cap["시가총액(억)"] = (df_cap["시가총액"] / 1e8).round(0).astype(int)

    df = df_price.join(df_cap[["시가총액(억)"]], how="inner")

    # ----------------------------
    # 최근 / 과거 데이터 추출
    # ----------------------------
    recent = df.iloc[-1]
    past_20 = df.iloc[-20]
    past_60 = df.iloc[-60]

    # ----------------------------
    # 지표 계산
    # ----------------------------
    거래대금증가율_20 = (
        (recent["거래대금(억)"] - past_20["거래대금(억)"]) / past_20["거래대금(억)"]
    ) * 100
    수익률_20 = ((recent["종가"] - past_20["종가"]) / past_20["종가"]) * 100

    거래대금증가율_60 = (
        (recent["거래대금(억)"] - past_60["거래대금(억)"]) / past_60["거래대금(억)"]
    ) * 100
    수익률_60 = ((recent["종가"] - past_60["종가"]) / past_60["종가"]) * 100

    results.append(
        {
            "날짜": df.index[-1].date(),
            "종목코드": stock_code,
            "종목명": stock.get_market_ticker_name(stock_code),
            "20일 거래대금증가율": round(거래대금증가율_20, 2),
            "20일 수익률": round(수익률_20, 2),
            "60일 거래대금증가율": round(거래대금증가율_60, 2),
            "60일 수익률": round(수익률_60, 2),
        }
    )

df_silver = pd.DataFrame(results)
print(df_silver)
