# Node.js 설치 방법

## 설치 확인

```bash
node --version
npm --version
npx --version
```

---

## 설치 방법

### Homebrew (macOS 권장)

```bash
brew install node
```

### nvm (버전 관리가 필요한 경우)

여러 Node.js 버전을 전환해야 할 때 유용합니다.

```bash
# nvm 설치
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# 터미널 재시작 후 설치 확인
nvm --version

# 최신 LTS 버전 설치
nvm install --lts

# 설치된 버전 확인
nvm list
```

---

## npx란?

`npx`는 Node.js에 포함된 패키지 실행 도구입니다. 전역 설치 없이 패키지를 바로 다운로드하여 실행합니다.

```bash
# 설치 없이 바로 실행
npx <패키지명>

# 설치 확인 프롬프트 자동 승인
npx -y <패키지명>
```

MCP 서버처럼 일회성으로 실행되는 도구에 주로 사용됩니다.
