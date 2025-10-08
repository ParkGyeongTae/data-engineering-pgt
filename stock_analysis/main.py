"""
uv run python stock_analysis/main.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pykrx")

from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from pykrx import stock

today = datetime.now()
_today = today.strftime("%Y%m%d")
_one_year_ago = (today - relativedelta(years=1)).strftime("%Y%m%d")

results = []

stock_codes = [
    "005930",  # 삼성전자
    "000660",  # 하이닉스
    "035420",  # 네이버
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

    # --------------------------------------------
    # 평균값 계산
    # --------------------------------------------
    recent = df.iloc[-10:].mean()  # 최근 5일 평균
    today_row = df.iloc[-1]  # 오늘
    yesterday_row = df.iloc[-2]  # 하루 전
    past_20 = df.iloc[-30:-20].mean()
    past_60 = df.iloc[-70:-60].mean()
    past_120 = df.iloc[-130:-120].mean()
    past_200 = df.iloc[-210:-200].mean()

    # --------------------------------------------
    # 증가율 계산 함수
    # --------------------------------------------
    def calc_rate(recent_val, past_val):
        return ((recent_val - past_val) / past_val) * 100 if past_val != 0 else 0

    # --------------------------------------------
    # 각 기간별 거래대금 증가율 & 수익률
    # --------------------------------------------
    def make_metrics(past):
        거래대금증가율 = calc_rate(recent["거래대금(억)"], past["거래대금(억)"])
        수익률 = calc_rate(recent["종가"], past["종가"])
        return 거래대금증가율, 수익률

    # 각 기준일별 계산
    거래대금증가율_20, 수익률_20 = make_metrics(past_20)
    거래대금증가율_60, 수익률_60 = make_metrics(past_60)
    거래대금증가율_120, 수익률_120 = make_metrics(past_120)
    거래대금증가율_200, 수익률_200 = make_metrics(past_200)

    # 오늘 기준 계산 (전일 대비)
    오늘_거래대금증가율 = calc_rate(
        today_row["거래대금(억)"], yesterday_row["거래대금(억)"]
    )
    오늘_수익률 = calc_rate(today_row["종가"], yesterday_row["종가"])

    # --------------------------------------------
    # 결과 저장
    # --------------------------------------------
    results.append(
        {
            "날짜": df.index[-1].date(),
            "종목코드": stock_code,
            "종목명": stock.get_market_ticker_name(stock_code),
            "오늘 종가": int(today_row["종가"]),
            "오늘 거래대금(억)": int(today_row["거래대금(억)"]),
            "오늘 거래대금증가율(%)": round(오늘_거래대금증가율, 2),
            "오늘 수익률(%)": round(오늘_수익률, 2),
            # 20일 기준
            "20일 거래대금증가율(%)": round(거래대금증가율_20, 2),
            "20일 수익률(%)": round(수익률_20, 2),
            # 60일 기준
            "60일 거래대금증가율(%)": round(거래대금증가율_60, 2),
            "60일 수익률(%)": round(수익률_60, 2),
            # 120일 기준
            "120일 거래대금증가율(%)": round(거래대금증가율_120, 2),
            "120일 수익률(%)": round(수익률_120, 2),
            # 200일 기준
            "200일 거래대금증가율(%)": round(거래대금증가율_200, 2),
            "200일 수익률(%)": round(수익률_200, 2),
        }
    )

# --------------------------------------------
# CSV 저장
# --------------------------------------------
df_silver = pd.DataFrame(results)
df_silver.to_csv("stock_analysis/silver.csv", index=False, encoding="utf-8-sig")
print("\n✅ 'stock_analysis/silver.csv' 저장 완료!")

# --------------------------------------------
# 💡 Value vs Attention 매트릭스 (오늘 포함)
# --------------------------------------------
plt.figure(figsize=(11, 9))

stock_colors = {
    "삼성전자": "tab:blue",
    "SK하이닉스": "tab:orange",
    "NAVER": "tab:green",
}

period_markers = {
    "오늘": "P",
    "20": "o",
    "60": "s",
    "120": "^",
    "200": "D",
}

periods = ["200", "120", "60", "20", "오늘"]

for _, row in df_silver.iterrows():
    name = row["종목명"]
    color = stock_colors.get(name, "gray")

    for period in periods:
        x_col = (
            f"{period}일 거래대금증가율(%)"
            if period != "오늘"
            else "오늘 거래대금증가율(%)"
        )
        y_col = f"{period}일 수익률(%)" if period != "오늘" else "오늘 수익률(%)"

        plt.scatter(
            row[x_col],
            row[y_col],
            s=110 if period == "오늘" else 90,
            color=color,
            marker=period_markers[period],
            edgecolors="black",
            linewidth=0.5,
            alpha=0.8 if period == "오늘" else 0.6,
        )

        plt.text(
            row[x_col] + 1.2,
            row[y_col],
            f"{name}_{period}",
            fontsize=8,
            ha="left",
            va="center",
            color=color,
        )

# 기준선
plt.axhline(0, color="gray", linestyle="--", alpha=0.5)
plt.axvline(0, color="gray", linestyle="--", alpha=0.5)

# 제목 및 축
plt.title(
    "Value vs Attention Matrix (오늘 + 20·60·120·200일 기준)", fontsize=15, pad=15
)
plt.xlabel("거래대금증가율(%) → 투자자 관심도", fontsize=12)
plt.ylabel("수익률(%) → 기업 가치평가", fontsize=12)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()
