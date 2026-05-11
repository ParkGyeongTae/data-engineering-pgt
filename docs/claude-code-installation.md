# Claude Code 설치 가이드

Claude Code는 Anthropic이 만든 AI 기반 CLI 도구로, 터미널에서 Claude와 대화하며 코드 작성, 디버깅, Git 작업 등을 수행할 수 있습니다.

## 사전 요구사항

- Node.js 18 이상 (npm 설치 방식 사용 시)
- Claude.ai **Pro / Max / Team / Enterprise** 계정 또는 Anthropic Console API 계정
  - 무료 플랜은 Claude Code 사용 불가

## 설치 방법

### 방법 1. npm (권장 - 모든 OS)

```bash
npm install -g @anthropic-ai/claude-code
```

> `sudo` 사용 금지. 권한 문제가 발생하면 Node.js 설치 경로를 확인하세요.

### 방법 2. 네이티브 설치 스크립트

**macOS / Linux / WSL**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell)**

```powershell
irm https://claude.ai/install.ps1 | iex
```

### 방법 3. apt (Debian / Ubuntu)

```bash
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
  -o /etc/apt/keyrings/claude-code.asc
echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
  | sudo tee /etc/apt/sources.list.d/claude-code.list
sudo apt update
sudo apt install claude-code
```

## 로그인

설치 후 터미널에서 `claude`를 실행하면 최초 1회 로그인이 요구됩니다.

```bash
claude
```

- 브라우저가 자동으로 열리며 Claude.ai 계정으로 로그인
- 브라우저가 열리지 않으면 `c`를 눌러 로그인 URL을 복사

Anthropic Console(API 과금) 계정으로 로그인하려면:

```bash
claude auth login --console
```

## 프로젝트에서 시작하기

```bash
cd your-project
claude
```

프로젝트 첫 실행 시 `/init` 명령어로 초기 설정을 완료하면 Claude Code가 코드베이스 구조를 파악합니다.

```
> /init
```
