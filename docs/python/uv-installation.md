# uv 설치 방법

Rust로 작성된 빠른 Python 패키지 매니저입니다. `pip`, `venv`, `pyenv` 등을 대체합니다.

## 설치 확인

```bash
uv --version
```

---

## 설치 방법

### Homebrew (macOS 권장)

```bash
brew install uv
```

### 공식 설치 스크립트

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 업그레이드 방법

### Homebrew

```bash
brew upgrade uv
```

### 공식 설치 스크립트

```bash
uv self update
```

---

## 주요 명령어

### 프로젝트 초기화

```bash
# 새 프로젝트 생성
uv init <프로젝트명>

# 현재 디렉토리에서 초기화
uv init
```

### 의존성 관리

```bash
# 패키지 추가
uv add <패키지명>

# 패키지 제거
uv remove <패키지명>

# 의존성 설치 (pyproject.toml 기준)
uv sync
```

### 스크립트 실행

```bash
uv run python <파일명>.py
```

### Python 버전 관리

```bash
# Python 버전 설치
uv python install 3.13

# 프로젝트에서 사용할 버전 지정
uv python pin 3.13
```

---

## Python 버전 설정

프로젝트 루트의 `.python-version` 파일로 버전을 고정합니다.

```
3.13
```

`uv sync` 실행 시 해당 버전의 Python과 가상환경(`.venv`)을 자동으로 생성합니다.
