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
    # 평균값 계산 (최근 5일 / 20일 / 60일 / 120일 / 200일 전 5일 평균)
    # --------------------------------------------
    recent = df.iloc[-5:].mean()  # 최근 5일 평균
    today_row = df.iloc[-1]  # 오늘(가장 최근) 데이터
    past_20 = df.iloc[-25:-20].mean()
    past_60 = df.iloc[-65:-60].mean()
    past_120 = df.iloc[-125:-120].mean()
    past_200 = df.iloc[-205:-200].mean()

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
# CSV로 저장
# --------------------------------------------
df_silver = pd.DataFrame(results)
df_silver.to_csv("stock_analysis/silver.csv", index=False, encoding="utf-8-sig")
print("\n✅ 'stock_analysis/silver.csv' 저장 완료!")
# --------------------------------------------
# 시각화 (한 그래프에 수익률 + 거래대금증가율)
# --------------------------------------------
periods = ["200", "120", "60", "20", "오늘"]  # ← 오늘 추가

fig, ax1 = plt.subplots(figsize=(10, 6))

# 🔹 왼쪽 Y축: 수익률
for _, row in df_silver.iterrows():
    name = row["종목명"]
    returns = [
        row.get(f"{p}일 수익률(%)", 0) if p != "오늘" else 0 for p in reversed(periods)
    ]
    ax1.plot(periods, returns, marker="o", linewidth=2, label=f"{name} 수익률(%)")

ax1.set_xlabel("기간 (일)", fontsize=12)
ax1.set_ylabel("수익률(%)", fontsize=12, color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.grid(alpha=0.3)

# 🔸 오른쪽 Y축: 거래대금증가율
ax2 = ax1.twinx()
for _, row in df_silver.iterrows():
    name = row["종목명"]
    volumes = [
        (
            row.get(f"{p}일 거래대금증가율(%)", 0)
            if p != "오늘"
            else row["오늘 거래대금(억)"] / 1000
        )  # 임시 스케일로 표현
        for p in reversed(periods)
    ]
    ax2.plot(
        periods,
        volumes,
        marker="s",
        linestyle="--",
        linewidth=2,
        alpha=0.7,
        label=f"{name} 거래대금증가율(%)",
    )

ax2.set_ylabel("거래대금증가율(%)", fontsize=12, color="tab:orange")
ax2.tick_params(axis="y", labelcolor="tab:orange")

plt.title("📉 (좌→우: 장기→단기→오늘) 수익률 vs 거래대금증가율", fontsize=14)
fig.legend(loc="upper left", bbox_to_anchor=(0.08, 0.9))
plt.tight_layout()
plt.show()
