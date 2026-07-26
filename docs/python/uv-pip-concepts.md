# uv / pip 개념 정리

---

## 1. pip (Pip Installs Packages)

**한 줄 정의**
pip는 Python에 기본 내장된 패키지 관리자다.

**핵심 포인트**
- Python을 설치하면 기본적으로 함께 딸려온다 (별도 설치 불필요).
- [PyPI](https://pypi.org)에 등록된 패키지를 검색·설치·삭제한다.
- 설치한 패키지는 현재 활성화된 Python 환경(전역 또는 가상환경)의 `site-packages/`에 저장된다.
- 어떤 패키지가 필요한지는 보통 `requirements.txt`에 기록한다.
- 의존성 해결(dependency resolution) 속도가 느리고, 별도의 lock 파일 개념이 없어 "누구 환경에서는 되는데 내 환경에서는 안 되는" 문제가 생기기 쉽다.

**예시**
```bash
pip install pandas          # pandas 설치
pip install -r requirements.txt   # requirements.txt에 정의된 의존성 전체 설치
pip freeze > requirements.txt     # 현재 설치된 패키지 목록을 파일로 저장
pip uninstall pandas         # 패키지 제거
```

---

## 2. uv

**한 줄 정의**
uv는 Rust로 작성된 차세대 Python 패키지·프로젝트 관리자로, pip/venv/pyenv/pip-tools 등을 하나로 통합한 도구다.

**핵심 포인트**
- 별도 설치가 필요하다 (Homebrew 또는 공식 설치 스크립트). 설치 방법은 [uv-installation.md](uv-installation.md) 참고.
- 패키지 설치·의존성 해결 속도가 pip보다 수십~수백 배 빠르다 (Rust 기반 병렬 처리 + 캐싱).
- `pyproject.toml`로 의존성을 관리하고, `uv.lock`이라는 lock 파일로 정확한 버전을 고정한다 → 팀원 간 환경 재현이 보장된다.
- 가상환경(`.venv/`) 생성·Python 버전 설치까지 하나의 도구에서 처리한다 (pyenv + venv + pip 대체).
- 명령어 대부분이 pip와 1:1로 대응되어 학습 곡선이 낮다.

**예시**
```bash
uv add pandas                # 의존성 추가 (pyproject.toml + uv.lock 갱신)
uv sync                      # pyproject.toml/uv.lock 기준으로 의존성 설치
uv remove pandas              # 의존성 제거
uv run python main.py         # 가상환경 활성화 없이 스크립트 실행
```

---

## 3. pip와 uv 비교

| 구분 | pip | uv |
|---|---|---|
| 설치 여부 | Python에 기본 포함 | 별도 설치 필요 |
| 구현 언어 | Python | Rust |
| 설치 속도 | 느림 | 매우 빠름 (병렬 처리 + 캐싱) |
| 의존성 정의 | `requirements.txt` | `pyproject.toml` |
| 버전 고정(lock) | 없음 (freeze로 흉내만 가능) | `uv.lock`으로 정확히 고정 |
| 가상환경 관리 | 별도 도구(`venv`) 필요 | 내장 |
| Python 버전 관리 | 별도 도구(`pyenv`) 필요 | 내장 (`uv python`) |
| 대체 범위 | 패키지 설치만 | pip + venv + pyenv + pip-tools |

---

## 4. 왜 requirements.txt 대신 pyproject.toml + lock 파일인가

**문제**: `requirements.txt`는 "설치할 패키지 이름과 (때로는) 버전"만 적혀 있다. `pandas` 같은 패키지는 내부적으로 `numpy` 등 여러 하위 의존성을 함께 설치하는데, 이 하위 의존성들의 정확한 버전까지는 고정되지 않는다. 그래서 같은 `requirements.txt`로 설치해도 시점에 따라, 또는 사람마다 조금씩 다른 버전 조합이 설치될 수 있다.

**해결**: uv는 실제로 설치된 모든 패키지(직접 의존성 + 하위 의존성)의 정확한 버전과 해시를 `uv.lock`에 기록한다. `uv sync`를 실행하면 이 lock 파일 그대로 재현되므로, 누가 언제 설치하든 동일한 환경이 보장된다.

- `pyproject.toml`: "무엇을 쓸지"에 대한 선언 (사람이 편집)
- `uv.lock`: "정확히 무엇이 설치됐는지"에 대한 스냅샷 (uv가 자동 생성, 사람이 직접 편집하지 않음)

---

## 5. 이 레포에서의 사용 원칙

이 레포는 패키지 매니저로 `uv`를 사용한다 (`CLAUDE.md` 참고).

```bash
uv sync                       # 의존성 설치
uv run python stock_analysis/main.py   # 스크립트 실행
uv add <패키지명>              # 패키지 추가
```

- `pip install`로 직접 설치하지 않는다 → `pyproject.toml`/`uv.lock`에 반영되지 않아 팀 재현성이 깨진다.
- Python 버전은 `.python-version` 파일 기준 (현재 3.13+).

---

## 6. 확인 질문

1. pip와 uv의 가장 큰 차이는 무엇인가?
2. `requirements.txt`에는 없고 `uv.lock`에는 있는 정보는 무엇인가?
3. `uv sync`를 실행하면 내부적으로 어떤 일이 일어나는가?
4. 이 레포에서 새 패키지를 추가할 때 `pip install` 대신 `uv add`를 써야 하는 이유는?
5. `pyproject.toml`과 `uv.lock`의 역할 차이는?

---

## 참고

- uv 설치/업그레이드 방법은 [uv-installation.md](uv-installation.md) 참고
- PyPI: https://pypi.org
