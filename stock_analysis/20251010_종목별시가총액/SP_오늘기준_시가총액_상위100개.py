"""
uv run python stock_analysis/20251010_종목별시가총액/SP_오늘기준_시가총액_상위100개.py
uv run streamlit run stock_analysis/20251010_종목별시가총액/SP_오늘기준_시가총액_상위100개_streamlit.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="yfinance")

from datetime import datetime

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_top_sp500_by_mcap(n=100):
    """S&P 500 시가총액 상위 n개를 가져옵니다. (기준: 오늘)"""
    # S&P 500 티커 리스트 가져오기
    sp500_tickers = yf.Tickers("^GSPC")

    # S&P 500 구성 종목들 (주요 종목들 상위 100개)
    major_tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "NVDA",
        "META",
        "TSLA",
        "BRK-B",
        "UNH",
        "JNJ",
        "V",
        "PG",
        "JPM",
        "MA",
        "HD",
        "CVX",
        "LLY",
        "PFE",
        "ABBV",
        "BAC",
        "KO",
        "AVGO",
        "PEP",
        "TMO",
        "COST",
        "WMT",
        "MRK",
        "ABT",
        "ACN",
        "DHR",
        "VZ",
        "ADBE",
        "NFLX",
        "CRM",
        "TXN",
        "QCOM",
        "NKE",
        "PM",
        "RTX",
        "HON",
        "UNP",
        "IBM",
        "SPGI",
        "LOW",
        "AMGN",
        "CAT",
        "GE",
        "AXP",
        "BKNG",
        "SBUX",
        "GS",
        "MMM",
        "BA",
        "DIS",
        "ORCL",
        "INTU",
        "AMD",
        "NOW",
        "ISRG",
        "GILD",
        "MDT",
        "PYPL",
        "T",
        "CMCSA",
        "COP",
        "LMT",
        "UPS",
        "ELV",
        "BLK",
        "SYK",
        "ADP",
        "CI",
        "SO",
        "DUK",
        "NEE",
        "PLD",
        "EQIX",
        "ICE",
        "SHW",
        "ITW",
        "EMR",
        "APD",
        "ETN",
        "ECL",
        "AON",
        "SPG",
        "CL",
        "FDX",
        "NSC",
        "GD",
        "AEP",
        "EXC",
        "XOM",
        "PEG",
        "SRE",
        "WEC",
        "ES",
        "AWK",
        "A",
        "CHTR",
        "CME",
        "COO",
        "CTAS",
        "D",
        "DE",
        "FIS",
        "FISV",
        "HCA",
        "HUM",
        "IDXX",
        "ILMN",
        "ISRG",
        "J",
        "KLAC",
        "LHX",
        "LIN",
        "LRCX",
        "MCD",
        "MDLZ",
        "MRNA",
        "MU",
        "NOC",
        "PCAR",
        "PNC",
        "REGN",
        "ROP",
        "SNPS",
        "TGT",
        "TJX",
        "TMO",
        "TRV",
        "TXN",
        "VRSK",
        "WBA",
        "ZTS",
    ]

    # 각 종목의 시가총액 정보 가져오기
    data = []
    for ticker in major_tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            market_cap = info.get("marketCap", 0)
            company_name = info.get("longName", ticker)

            if market_cap > 0:
                data.append(
                    {"종목코드": ticker, "종목명": company_name, "시가총액": market_cap}
                )
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue

    # DataFrame 생성
    df = pd.DataFrame(data)

    # 달러를 원화로 변환 (1달러 = 1400원 가정)
    usd_to_krw = 1400
    df["시가총액(조)"] = (df["시가총액"] * usd_to_krw / 1e12).round(3)

    # 상위 n개 종목들의 시가총액 합계 계산
    top_n_mcap = df["시가총액"].head(n).sum()
    df["시가총액비율(%)"] = (df["시가총액"] / top_n_mcap * 100).round(3)

    out = (
        df.sort_values("시가총액", ascending=False)
        .loc[:, ["종목코드", "종목명", "시가총액(조)", "시가총액비율(%)"]]
        .head(n)
        .reset_index(drop=True)
    )
    out.insert(0, "순위", out.index + 1)

    today = datetime.now().strftime("%Y%m%d")
    return today, out


def generate_theme(company_name: str) -> str:
    """OpenAI를 이용해 종목별 투자 테마 생성"""
    prompt = f"""
    아래 회사명에 대해 현재 미국 주식시장에서 가장 관련 있는 '투자 테마'를 3개 이하로 요약해줘.
    현재 시간은 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}입니다.
    예시는 다음과 같아:
    - Apple → 스마트폰, AI, 서비스
    - Microsoft → 클라우드, AI, 생산성소프트웨어
    - Tesla → 전기차, 자율주행, 에너지저장
    - NVIDIA → AI반도체, 데이터센터, 게임

    회사명: {company_name}
    회사와 가장 관련있는 순서대로 작성해줘.
    출력은 '테마1, 테마2, 테마3' 형식의 띄어쓰기 없는 문자열로만 작성해.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"생성 실패: {e}"


def split_themes(theme_str: str):
    """쉼표로 구분된 테마 문자열을 최대 3개 컬럼으로 분리"""
    parts = [t.strip() for t in theme_str.replace("·", ",").split(",") if t.strip()]
    parts = (parts + [""] * 3)[:3]
    return pd.Series(parts, index=["1순위테마", "2순위테마", "3순위테마"])


if __name__ == "__main__":
    # ✅ 오늘 기준 데이터
    date, top100 = get_top_sp500_by_mcap(n=100)

    # ✅ OpenAI로 각 종목의 테마 생성
    themes = []
    for name in top100["종목명"]:
        theme = generate_theme(name)
        print(f"{name}: {theme}")
        themes.append(theme)

    top100["테마문장"] = themes
    theme_df = top100["테마문장"].apply(split_themes)
    top100 = pd.concat([top100.drop(columns=["테마문장"]), theme_df], axis=1)

    print(f"\n[기준일] {date}")
    pd.set_option("display.max_rows", 200)
    print(top100.to_string(index=False))

    output_path = f"stock_analysis/20251010_종목별시가총액/SP_오늘기준_시가총액_상위100개_{date}.csv"
    top100.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n✅ 결과가 '{output_path}' 파일로 저장되었습니다.")
