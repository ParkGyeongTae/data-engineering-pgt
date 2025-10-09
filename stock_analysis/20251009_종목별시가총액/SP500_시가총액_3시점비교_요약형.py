import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup


# ✅ S&P500 종목 목록 가져오기 (Wikipedia)
def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df["Symbol"].tolist()


# ✅ 시가총액 계산 함수
def get_today_top_sp500(n=10):
    tickers = get_sp500_tickers()
    data = []

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            name = info.get("shortName", ticker)
            mcap = info.get("marketCap", 0)
            data.append(
                {
                    "티커": ticker,
                    "종목명": name,
                    "시가총액(억달러)": round(mcap / 1e8, 1),
                }
            )
        except Exception:
            continue

    df = pd.DataFrame(data)
    df = (
        df.sort_values("시가총액(억달러)", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
    df.insert(0, "순위", df.index + 1)
    return df


# ✅ 실행
if __name__ == "__main__":
    top10 = get_today_top_sp500(10)
    pd.set_option("display.max_rows", 20)
    print("\n📈 오늘 기준 S&P500 시가총액 상위 10개")
    print(top10.to_string(index=False))
