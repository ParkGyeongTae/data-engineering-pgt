# GitHub MCP 설정 방법

GitHub 이슈, PR, 코드 검색 등 GitHub 작업을 Claude가 직접 수행할 수 있게 해주는 MCP입니다. `@modelcontextprotocol/server-github` 패키지를 `npx`로 실행하며, 이슈/PR 생성·조회, 파일 조회·수정, 코드/이슈 검색 등의 툴을 제공합니다.

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

> 발급받은 토큰은 비밀번호와 동일하게 취급합니다. 아래 어떤 방법을 쓰더라도 토큰이 포함된 파일은 git에 커밋하지 않습니다.

## 설정 범위(scope) 3가지

`claude mcp add`의 `-s/--scope` 옵션 기준으로 설정 범위가 3가지로 나뉩니다. 저장 위치와 공유 여부가 다르므로 용도에 맞게 선택합니다.

| 범위 | 적용 대상 | 저장 위치 | 다른 사람과 공유 |
|------|-----------|-----------|------------------|
| `local` (기본값) | 지금 이 프로젝트 디렉터리에서만 | `~/.claude.json` (`projects["<경로>"].mcpServers`) | ❌ 나만 |
| `user` | 모든 프로젝트 (글로벌) | `~/.claude.json` (최상위 `mcpServers`) | ❌ 나만 |
| `project` | 지금 이 프로젝트 | 프로젝트 루트 `.mcp.json` | ✅ git 커밋 시 팀과 공유 |

> `-s`를 생략하면 `local`이 기본값으로 적용됩니다. GitHub 토큰처럼 민감한 값은 대부분 `local` 또는 `user` 범위로 등록하고, `project` 범위(`.mcp.json`)에는 토큰을 직접 넣지 않는 것이 안전합니다.

---

## 방법 1. CLI 명령어 (권장)

```bash
# local: 이 프로젝트에서만, 나만 (scope 생략 시 기본값)
claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here -- npx -y @modelcontextprotocol/server-github

# user: 모든 프로젝트에서, 나만 (글로벌)
claude mcp add github -s user -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here -- npx -y @modelcontextprotocol/server-github

# project: 이 프로젝트, .mcp.json에 저장되어 팀과 공유 (토큰은 넣지 않는 것을 권장)
claude mcp add github -s project -- npx -y @modelcontextprotocol/server-github
```

확인 및 삭제:

```bash
claude mcp list          # 등록된 MCP 서버와 연결 상태 확인
claude mcp get github    # 특정 서버의 scope, 상태 확인
claude mcp remove github -s user   # 등록한 scope를 정확히 지정해서 제거
```

## 방법 2. `~/.claude.json` 직접 편집 (`user` 범위)

`~/.claude.json`의 최상위 `mcpServers` 항목에 아래 내용을 추가합니다.

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

> `~/.claude.json`에는 개인 설정, 세션 캐시, 그리고 다른 프로젝트의 `local` scope MCP 설정까지 함께 들어있는 큰 파일입니다. 토큰이 평문으로 저장되므로 파일 권한과 백업 위치에 주의하고, 직접 편집할 때는 JSON 문법 오류가 나지 않게 특히 조심합니다.

## 방법 3. `.mcp.json` (`project` 범위)

프로젝트 루트에 `.mcp.json` 파일을 생성합니다. git에 커밋하면 팀원과 설정을 공유할 수 있습니다.

> **주의:** 토큰이 포함된 `.mcp.json`은 절대 git에 커밋하지 않습니다. 팀과 공유해야 한다면 `env` 값을 직접 넣는 대신 `"${GITHUB_PERSONAL_ACCESS_TOKEN}"`처럼 환경 변수 참조로 작성하고, 각자 로컬 셸 환경 변수로 토큰을 관리하게 합니다.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

> 협업자가 이 파일이 포함된 프로젝트를 처음 열면, `.mcp.json`의 서버는 바로 연결되지 않고 `claude mcp list`에 `⏸ Pending approval`로 표시됩니다. Claude Code가 처음 실행될 때 승인 여부를 묻고, 승인해야 연결됩니다. 이 승인 이력을 초기화하려면 `claude mcp reset-project-choices`를 실행합니다.

## 적용

설정 파일 수정 후 Claude Code를 재시작하면 적용됩니다. 정상 연결됐는지는 `claude mcp list`로 확인합니다.
