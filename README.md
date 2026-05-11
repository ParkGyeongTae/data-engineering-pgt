# data-engineering-pgt

데이터 엔지니어링 관련 학습, 실무 경험, 프로젝트를 기록하는 개인 저장소입니다.

## 구조

```
data-engineering-pgt/
├── data-engineering/          # 데이터 엔지니어링 실습 및 학습
│   ├── docker/                # 인프라 환경 구성 (ELK, Spark, Ubuntu)
│   ├── ecommerce-behavior-data/  # 이커머스 행동 데이터 분석 (Scala/Spark)
│   └── online-course/         # 강의 실습 코드 (Java, Spring)
└── stock_analysis/            # 주식 데이터 분석 (Python)
```

## 섹션별 설명

### data-engineering
데이터 엔지니어링 핵심 기술 학습 및 실습 내용을 담고 있습니다.

- **docker**: ELK Stack, Spark, Ubuntu 등 로컬 데이터 인프라 환경 구성
- **ecommerce-behavior-data**: Scala + Spark 기반 이커머스 사용자 행동 데이터 파이프라인
- **online-course**: 강의를 통해 학습한 Java, Spring 코드

### stock_analysis
pykrx, FinanceDataReader 등을 활용한 국내 주식 시장 데이터 수집 및 분석

## 환경 설정

Python 프로젝트는 `uv`로 의존성을 관리합니다.

```bash
uv init
uv add pykrx finance-datareader yfinance pandas matplotlib plotly streamlit
uv run python stock_analysis/main.py
```
