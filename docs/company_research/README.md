# Company Research

**투자 판단**을 위한 회사 분석 문서를 모아두는 폴더입니다.
"이 회사에 투자할 만한가?"를 스스로 정리하는 것이 목적이며, 개발/기술 스택 조사는 다루지 않습니다.

> ⚠️ 여기 정리된 내용은 개인 학습·기록용이며 투자 권유가 아닙니다. 투자 판단과 책임은 본인에게 있습니다.
>
> 커버리지는 **미국 상장 기업(NYSE/NASDAQ, USD 표시) 위주**를 기본 전제로 합니다. 템플릿의 재무·거버넌스 용어(GAAP/Non-GAAP, 위임장(Proxy Statement) 등)도 이 전제 위에서 작성되어 있습니다 — 비-US 기업을 예외적으로 다룰 경우 해당 용어를 그 회사 문서 안에서 직접 치환하고 각주로 남기세요(예: GAAP→IFRS, 위임장→Compensation Report).

---

## 📁 폴더 구조

**산업/섹터 폴더** 아래에 회사 폴더를 둡니다.

```
company_research/
├── README.md            # (이 파일) 공통 규칙
├── glossary.md           # PER/PBR/DCF/WACC 등 문서 전반에서 쓰는 용어 정리
├── _template/            # 새 회사/섹터 추가 시 복사해서 쓰는 템플릿 모음
│   ├── company/          # 회사 폴더에 복사하는 템플릿 (숫자 접두사 = 읽는 순서)
│   │   ├── 01_overview.md
│   │   ├── 02_history.md
│   │   ├── 03_ceo.md
│   │   ├── 04_financials.md
│   │   ├── 05_metrics.md
│   │   ├── 06_valuation.md
│   │   └── 07_investment.md
│   └── sector/           # 섹터 폴더에 복사하는 템플릿
│       └── 01_comparison.md
├── electronic_design_automation/   # 섹터 폴더명은 풀어 쓴 소문자 스네이크케이스
│   ├── comparison.md    # (선택) 섹터 내 회사 비교 — 2개사 이상일 때만
│   ├── synopsys/
│   ├── cadence_design_systems/
│   └── siemens/
└── <sector>/
    ├── comparison.md
    └── <company-name>/
        └── ...
```

- 섹터 폴더명: **풀어 쓴 소문자 스네이크케이스** (예: `electronic_design_automation`, `semiconductor`, `cloud_infrastructure`) — 약어보다 명확한 전체 표기 우선
- 회사 폴더명: **회사명 소문자 스네이크케이스** (예: `synopsys`, `nvidia`, `apple`)
- 복합기업은 "관심 이유"가 되는 사업 기준 섹터에 배치 (예: Siemens → `electronic_design_automation/`)
- 처음엔 `01_overview.md`만 있어도 됨. 분석이 깊어지면 아래 표대로 분리.

---

## 📄 파일별 역할 (통일 규칙)

| 파일명 | 담는 내용 | 필수 여부 |
|--------|-----------|-----------|
| `01_overview.md` | 회사 개요, 사업 모델(**어떻게 돈을 버는가**), 산업 내 위치 | ✅ 필수 |
| `02_history.md` | 창업부터 현재까지의 연혁·주요 이벤트 | 선택 |
| `03_ceo.md` | CEO/경영진 이력, 경영 스타일, 보상·지분, 시장 평가 | 선택 |
| `04_financials.md` | 성장성·수익성·재무건전성·주주환원에 대한 **서술형 해석**. 숫자는 `05_metrics.md`를 인용만 하고 여기서 새로 표를 만들지 않는다 | 선택 |
| `05_metrics.md` | 최근 3개년+올해(연간) / 최근 6개 분기의 매출·영업이익·PER·PBR·유동비율·부채비율·FCF·배당(DPS) 등 **원자료 수치표** (평균·중앙값 비교용). 회사 관련 모든 문서가 참조하는 단일 출처(source of truth) | 선택 |
| `06_valuation.md` | PER/PBR/DCF/DDM 등 방법론별 적정주가 산정과 근거·가정·민감도. EPS·BPS·DPS 등은 `05_metrics.md`를 인용 | 선택 |
| `07_investment.md` | 투자 포인트(강점)·리스크·경쟁 해자·**투자 결론**. 밸류에이션 숫자는 `06_valuation.md`를 요약 인용만 한다 | 선택 |
| `news.md` | 최근 뉴스·이슈·실적 발표 등 시점성 메모. `_template/`에는 없음 — 필요할 때 회사 폴더에 직접 만들어 쓰는 자유 양식이라 번호를 붙이지 않음 | 선택 |
| `<sector>/comparison.md` | 같은 섹터 내 커버리지 기업 간 사업 포지셔닝·밸류에이션 비교와 종합 순위. `_template/sector/01_comparison.md`를 복사해서 씀 | 선택 (섹터 내 2개사 이상일 때 권장) |

> 파일명 앞 숫자(01~07)는 **읽는 순서**(개요→역사→경영진→해석→원자료→밸류에이션→결론)를 그대로 나타냅니다. 새 회사 폴더는 `_template/company/`를 복사해서 만들기 때문에 숫자도 그대로 따라옵니다 — 기존에 이미 만들어둔 회사 폴더(번호 없는 파일명)까지 소급 적용하려면 별도로 리네이밍이 필요합니다.
> 회사마다 파일을 **똑같은 이름**으로 유지하면, 나중에 회사 간 비교가 쉬워집니다.
> `05_metrics.md`가 원자료의 유일한 출처입니다. `04_financials.md`·`06_valuation.md`·`07_investment.md`는 숫자를 다시 채우지 말고 `05_metrics.md` 값을 인용해 해석만 쓰세요. `06_valuation.md`에서 미래 추정치(E)처럼 `05_metrics.md`에 아직 없는 값을 쓸 때만 그 문서에 직접 근거를 남기고, 확정치는 항상 `05_metrics.md`로 되돌아가 채우세요.
> 같은 폴더의 다른 문서들은 서로 전부 링크하는 것(풀 메시)이 기본값입니다 — 없는 문서만 링크에서 빼세요.
> PER·PBR·DCF·WACC·%p 등 용어가 낯설면 [`glossary.md`](./glossary.md)를 먼저 보세요.

---

## ✍️ 작성 규칙

- 모든 문서는 **최상단에 `#` 제목 + `>` 한 줄 요약(투자 관점)**으로 시작
- 재무·실적 수치는 **기준 시점을 반드시 명시** (예: "FY2026 1분기 기준")
- 사실 정보(실적·인수·인물)는 **출처 링크**를 문서 하단 "참고 자료"에 남기기
- 주관적 판단(투자 결론)과 객관적 사실(재무 수치)을 **섞지 말고 구분**해서 적기
- 회계연도(FY)처럼 헷갈리는 개념은 각주로 설명
- 문서 맨 아래에 `*작성일: YYYY-MM-DD*` 표기

---

## ➕ 새 회사 추가 방법

```bash
# 1. 템플릿 복사
cp -r docs/company_research/_template/company docs/company_research/<sector>/<company-name>

# 2. 파일 내용 채우기
# 3. 필요 없는 파일은 삭제 (01_overview.md는 유지 권장)

# 4. 같은 섹터에 회사가 2개 이상이면 비교 문서도 추가
cp docs/company_research/_template/sector/01_comparison.md docs/company_research/<sector>/comparison.md
```

---

*작성일: 2026-08-01*
