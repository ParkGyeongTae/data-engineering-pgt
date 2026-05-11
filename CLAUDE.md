# CLAUDE.md

이 레포지토리는 데이터 엔지니어링 관련 학습, 실무 경험, 프로젝트를 기록하는 개인 저장소입니다.

## 레포 구조

```
data-engineering-pgt/
├── data-engineering/          # 데이터 엔지니어링 실습
│   ├── docker/                # ELK, Spark, Ubuntu 환경 구성
│   ├── ecommerce-behavior-data/  # Scala + Spark 파이프라인
│   └── online-course/         # 강의 실습 (Java, Spring)
├── stock_analysis/            # 주식 데이터 분석 (Python)
└── docs/                      # 학습 및 실무 지식 문서
    ├── claude/                # Claude Code 관련
    └── git/                   # Git 관련
```

## Python 환경

패키지 매니저로 `uv`를 사용합니다.

```bash
# 의존성 설치
uv sync

# 스크립트 실행
uv run python stock_analysis/main.py

# 패키지 추가
uv add <패키지명>
```

Python 버전: `.python-version` 파일 참고 (현재 3.13+)

주요 라이브러리: `pykrx`, `finance-datareader`, `yfinance`, `pandas`, `streamlit`, `plotly`

## 문서 작성 규칙

- 새로운 지식/경험은 `docs/` 하위 주제별 폴더에 `.md` 파일로 작성
- 폴더 구조 예시: `docs/spark/`, `docs/kafka/`, `docs/airflow/`
- 파일명은 내용을 명확히 드러내는 소문자 케밥케이스 사용 (예: `pr-checkout.md`)

## 커밋 규칙

```
docs: 문서 추가 또는 수정
feat: 새로운 분석/스크립트 추가
fix: 버그 수정
refactor: 코드 개선
```

## 주의사항

- `.env` 파일에 API 키 등 민감 정보 보관 — 절대 커밋 금지
- `.venv/`, `data/` 등 대용량 파일은 gitignore 처리됨
