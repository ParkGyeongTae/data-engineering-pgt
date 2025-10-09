"""
uv run python stock_analysis/20251009_종목별시가총액/KOSPI_시가총액_3시점비교_요약형.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pykrx")

from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from openai import OpenAI
from pykrx import stock

load_dotenv()
client = OpenAI()


def get_top_kospi_by_mcap(n=10, years_ago=0):
    """코스피 시가총액 상위 n개를 가져옵니다. (기준: years_ago년 전)"""
    today = datetime.now()
    target_date = (today - relativedelta(years=years_ago)).strftime("%Y%m%d")
    date = stock.get_nearest_business_day_in_a_week(target_date)
    df = (
        stock.get_market_cap_by_ticker(date, market="KOSPI")
        .reset_index()
        .rename(columns={"티커": "종목코드"})
    )
    df["종목명"] = df["종목코드"].map(stock.get_market_ticker_name)
    df["시가총액(조)"] = (df["시가총액"] / 1e12).round(1)  # 소수점 첫째 자리 반올림
    df = df.sort_values("시가총액", ascending=False).head(n).reset_index(drop=True)
    total_mcap = df["시가총액(조)"].sum()
    df["비율(%)"] = (df["시가총액(조)"] / total_mcap * 100).round(1)
    df.insert(0, "순위", df.index + 1)
    return date, df


def generate_theme(company_name: str) -> str:
    """OpenAI를 이용해 종목별 대표 테마(1개) 생성"""
    prompt = f"""
    아래 회사명에 대해 현재 한국 주식시장에서 가장 대표적인 '투자 테마'를 1개로 요약해줘.
    예시는 단지 참고용이며, 실제 출력에서는 '→' 기호나 회사명을 포함하지 마.
    출력은 테마 이름 한 개만 작성해.

    예시:
    삼성전자 → 반도체
    LG화학 → 2차전지
    NAVER → 인터넷 플랫폼
    한화에어로스페이스 → 방산

    회사명: {company_name}
    출력: 테마 이름만 작성 (예: "반도체")
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"생성 실패: {e}"


def clean_theme(theme: str) -> str:
    """불필요한 기호나 회사명 제거"""
    for symbol in ["→", "-", ":", "–"]:
        theme = theme.replace(symbol, "")
    return theme.strip()


def build_theme_table(n=10):
    """3년전 / 2년전 / 1년전 / 현재 상위 n개 종목 + 테마 + 시가총액(비율)"""
    result_frames = []
    year_offsets = [3, 2, 1, 0]
    year_labels = {3: "3년전", 2: "2년전", 1: "1년전", 0: "오늘"}

    for offset in year_offsets:
        date, df = get_top_kospi_by_mcap(n=n, years_ago=offset)
        print(f"\n📅 [{year_labels[offset]} 기준일] {date}")

        themes = []
        for name in df["종목명"]:
            theme = generate_theme(name)
            theme = clean_theme(theme)
            print(f"{name}: {theme}")
            themes.append(theme)
        df["대표테마"] = themes

        # ✅ 종목(테마) 형식으로 결합
        df[f"{year_labels[offset]}_종목(테마)"] = (
            df["종목명"] + "(" + df["대표테마"] + ")"
        )

        # ✅ 시가총액(비율) 형식으로 결합
        df[f"{year_labels[offset]}_시가총액(비율)"] = (
            df["시가총액(조)"].astype(int).astype(str)
            + "조("
            + df["비율(%)"].astype(int).astype(str)
            + "%)"
        )

        # ✅ 필요한 컬럼만 선택
        df = df.loc[
            :,
            [
                "순위",
                f"{year_labels[offset]}_종목(테마)",
                f"{year_labels[offset]}_시가총액(비율)",
            ],
        ]
        result_frames.append(df)

    # 순위를 기준으로 병합
    merged = result_frames[0]
    for df in result_frames[1:]:
        merged = pd.merge(merged, df, on="순위", how="outer")

    return merged


if __name__ == "__main__":
    top10_compare = build_theme_table(n=20)

    print("\n✅ KOSPI 시가총액 상위 10개 비교")
    pd.set_option("display.max_rows", 50)
    print(top10_compare.to_string(index=False))

    # CSV 저장
    output_path = (
        "stock_analysis/20251009_종목별시가총액/KOSPI_TOP10_3시점비교_요약형.csv"
    )
    top10_compare.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n💾 결과가 '{output_path}' 파일로 저장되었습니다.")
