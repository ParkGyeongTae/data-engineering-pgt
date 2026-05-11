# GitHub MCP 설정 방법

GitHub 이슈, PR, 코드 검색 등 GitHub 작업을 Claude에서 직접 수행할 수 있게 해주는 MCP입니다.

## 사전 준비 1: Node.js 설치

`npx`는 Node.js에 포함된 도구로, GitHub MCP 실행에 필요합니다.

```bash
# 설치 확인
node --version
npx --version
```

설치되어 있지 않다면 Homebrew로 설치합니다.

```bash
brew install node
```

---

## 사전 준비 2: Personal Access Token 발급

[GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens) 에서 토큰을 발급받습니다.

필요한 권한: `repo`, `read:org`, `read:user`

## 추가 방법 3가지

| 방법 | 적용 범위 | 파일 |
|------|-----------|------|
| `~/.claude.json` | 전체 프로젝트 (글로벌) | 직접 편집 |
| `.mcp.json` | 해당 프로젝트만 | 프로젝트 루트에 생성 |
| CLI 명령어 | 글로벌 또는 프로젝트 | 터미널에서 실행 |

---

## 방법 1. `~/.claude.json` 직접 편집 (글로벌)

`~/.claude.json`의 `mcpServers` 항목에 아래 내용을 추가합니다.

```json
"mcpServers": {
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
    }
  }
}
```

## 방법 2. `.mcp.json` (프로젝트별)

프로젝트 루트에 `.mcp.json` 파일을 생성합니다. 해당 프로젝트에서만 적용되며, git에 커밋하면 팀과 공유할 수 있습니다.

> **주의:** 토큰이 포함된 `.mcp.json`은 절대 git에 커밋하지 않습니다.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## 방법 3. CLI 명령어

터미널에서 직접 추가할 수 있습니다.

```bash
# 글로벌 추가 (~/.claude.json에 저장)
claude mcp add github -s user -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here -- npx -y @modelcontextprotocol/server-github

# 프로젝트별 추가 (.mcp.json에 저장)
claude mcp add github -s project -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here -- npx -y @modelcontextprotocol/server-github
```

## 적용

설정 파일 수정 후 Claude Code를 재시작하면 적용됩니다.
