# Claude Code 설치 가이드

Claude Code는 Anthropic이 만든 AI 기반 CLI 도구로, 터미널에서 Claude와 대화하며 코드 작성, 디버깅, Git 작업 등을 수행할 수 있습니다.

## 사전 요구사항

- **OS**: macOS 13.0+ / Windows 10 1809+ (또는 Windows Server 2019+) / Ubuntu 20.04+ / Debian 10+ / Alpine Linux 3.19+
- **하드웨어**: RAM 4GB 이상, x64 또는 ARM64
- **계정**: Claude.ai **Pro / Max / Team / Enterprise** 계정 또는 Anthropic Console API 계정
  - 무료 플랜은 Claude Code 사용 불가
- **npm으로 설치할 경우**: Node.js 22 이상 필요 (v2.1.198 기준)
  - 실제 실행 파일은 플랫폼별 네이티브 바이너리이므로, Node.js는 설치 시에만 필요하고 런타임에는 사용되지 않음

## 설치 방법

### 방법 1. 네이티브 설치 스크립트 (권장 - 모든 OS)

**macOS / Linux / WSL**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell)**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows (CMD)**

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> 네이티브 설치는 백그라운드에서 자동으로 최신 버전을 유지합니다.

### 방법 2. Homebrew (macOS)

```bash
brew install --cask claude-code
```

> `claude-code`는 stable 채널(약 1주 지연), `claude-code@latest`는 최신 채널을 추적합니다. Homebrew 설치는 자동 업데이트되지 않으므로 `brew upgrade claude-code`로 직접 갱신해야 합니다.

### 방법 3. WinGet (Windows)

```powershell
winget install Anthropic.ClaudeCode
```

### 방법 4. npm (모든 OS, Node.js 22+ 필요)

```bash
npm install -g @anthropic-ai/claude-code
```

> `sudo` 사용 금지. 권한 문제가 발생하면 Node.js 설치 경로를 확인하세요.

### 방법 5. apt (Debian / Ubuntu)

```bash
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
  -o /etc/apt/keyrings/claude-code.asc
echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
  | sudo tee /etc/apt/sources.list.d/claude-code.list
sudo apt update
sudo apt install claude-code
```

> 키를 신뢰하기 전에 지문을 확인하세요: `gpg --show-keys /etc/apt/keyrings/claude-code.asc` → `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`
> `stable`을 `latest`로 바꾸면 최신 채널을 받습니다. Fedora/RHEL은 dnf, Alpine은 apk로 동일하게 설치 가능합니다.

## 설치 확인

```bash
claude --version   # 버전 확인
claude doctor       # 설치/설정 상태 진단
```

## 로그인

설치 후 터미널에서 `claude`를 실행하면 최초 1회 로그인이 요구됩니다.

```bash
claude
```

- 브라우저가 자동으로 열리며 로그인 진행
- 브라우저가 열리지 않으면 `c`를 눌러 로그인 URL을 복사
- 로그인 프롬프트에서 계정 유형(Claude.ai 구독, Claude Console, 3rd-party platform 등)을 선택
- 세션 중 재로그인은 `/login`, 로그아웃은 `/logout`
- 브라우저 로그인이 불가능한 CI/CD 환경 등에서는 `claude setup-token`으로 1년짜리 OAuth 토큰을 발급받아 `CLAUDE_CODE_OAUTH_TOKEN` 환경 변수로 사용

## 프로젝트에서 시작하기

```bash
cd your-project
claude
```

프로젝트 첫 실행 시 `/init` 명령어로 초기 설정을 완료하면 Claude Code가 코드베이스 구조를 파악합니다.

```
> /init
```
