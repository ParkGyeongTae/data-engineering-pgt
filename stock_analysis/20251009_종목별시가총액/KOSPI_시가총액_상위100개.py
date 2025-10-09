"""
uv run python stock_analysis/20251009_종목별시가총액/KOSPI_시가총액_상위100개.py
"""

# pylint: disable=non-ascii-name,wrong-import-position

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pykrx")

from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta  # ✅ 추가
from dotenv import load_dotenv
from openai import OpenAI
from pykrx import stock

load_dotenv()
client = OpenAI()


def get_top_kospi_by_mcap(n=100, years_ago=1):
    """코스피 시가총액 상위 n개를 가져옵니다. (기준: years_ago년 전)"""
    today = datetime.now()
    target_date = (today - relativedelta(years=years_ago)).strftime("%Y%m%d")
    date = stock.get_nearest_business_day_in_a_week(target_date)  # ✅ 1년 전 영업일
    df = (
        stock.get_market_cap_by_ticker(date, market="KOSPI")
        .reset_index()
        .rename(columns={"티커": "종목코드"})
    )
    df["종목명"] = df["종목코드"].map(stock.get_market_ticker_name)
    df["시가총액(조)"] = (df["시가총액"] / 1e12).round(2)
    out = (
        df.sort_values("시가총액", ascending=False)
        .loc[:, ["종목코드", "종목명", "시가총액(조)"]]
        .head(n)
        .reset_index(drop=True)
    )
    out.insert(0, "순위", out.index + 1)
    return date, out


def generate_theme(company_name: str) -> str:
    """OpenAI를 이용해 종목별 투자 테마 생성"""
    prompt = f"""
    아래 회사명에 대해 현재 한국 주식시장에서 가장 관련 있는 '투자 테마'를 3개 이하로 요약해줘.
    현재 시간은 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}입니다.
    예시는 다음과 같아:
    - 삼성전자 → 반도체, AI 반도체, 시스템반도체
    - LG화학 → 2차전지, 친환경소재, 전기차
    - NAVER → 인터넷 플랫폼, AI, 콘텐츠
    - 한화에어로스페이스 → 방산, 우주항공, 로봇

    회사명: {company_name}
    출력은 '테마1, 테마2, 테마3' 형식의 문자열로만 작성해.
    가장 관련있는 순서대로 작성해줘.
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
    # ✅ 1년 전 기준 데이터
    date, top100 = get_top_kospi_by_mcap(n=10, years_ago=1)

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

    # 결과 CSV 저장
    output_path = f"stock_analysis/20251009_종목별시가총액/KOSPI_TOP100_{date}.csv"
    top100.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n✅ 결과가 '{output_path}' 파일로 저장되었습니다.")
