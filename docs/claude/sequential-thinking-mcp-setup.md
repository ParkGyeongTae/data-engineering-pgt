# sequential-thinking MCP 설정 방법

단계적 사고가 필요한 복잡한 작업에서 Claude의 추론 과정을 구조화해주는 MCP입니다. `sequentialthinking` 툴 하나를 제공하며, 문제를 여러 단계로 쪼개 생각하고 필요하면 이전 단계를 수정·재검토하면서 답을 다듬는 방식으로 동작합니다. `@modelcontextprotocol/server-sequential-thinking` 패키지를 `npx`로 실행하며, 별도 API 키나 인증이 필요 없습니다.

## 사전 준비: Node.js 설치

`npx`는 Node.js에 포함된 도구로, sequential-thinking MCP 실행에 필요합니다.

```bash
# 설치 확인
node --version
npx --version
```

설치되어 있지 않다면 Homebrew로 설치합니다.

```bash
brew install node
```

## 설정 범위(scope) 3가지

`claude mcp add`의 `-s/--scope` 옵션 기준으로 설정 범위가 3가지로 나뉩니다. 저장 위치와 공유 여부가 다르므로 용도에 맞게 선택합니다.

| 범위 | 적용 대상 | 저장 위치 | 다른 사람과 공유 |
|------|-----------|-----------|------------------|
| `local` (기본값) | 지금 이 프로젝트 디렉터리에서만 | `~/.claude.json` (`projects["<경로>"].mcpServers`) | ❌ 나만 |
| `user` | 모든 프로젝트 (글로벌) | `~/.claude.json` (최상위 `mcpServers`) | ❌ 나만 |
| `project` | 지금 이 프로젝트 | 프로젝트 루트 `.mcp.json` | ✅ git 커밋 시 팀과 공유 |

> `-s`를 생략하면 `local`이 기본값으로 적용됩니다. "글로벌로 설정한 줄 알았는데 다른 프로젝트에서 안 보인다"는 실수는 대부분 이 기본값 때문입니다. sequential-thinking은 민감 정보를 다루지 않으므로 편한 범위로 등록하면 되고, 여러 프로젝트에서 반복적으로 쓴다면 `user` 범위(글로벌)가 편합니다.

---

## 방법 1. CLI 명령어 (권장)

```bash
# local: 이 프로젝트에서만, 나만 (scope 생략 시 기본값)
claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking

# user: 모든 프로젝트에서, 나만 (글로벌)
claude mcp add sequential-thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking

# project: 이 프로젝트, .mcp.json에 저장되어 팀과 공유
claude mcp add sequential-thinking -s project -- npx -y @modelcontextprotocol/server-sequential-thinking
```

확인 및 삭제:

```bash
claude mcp list                          # 등록된 MCP 서버와 연결 상태 확인
claude mcp get sequential-thinking       # 특정 서버의 scope, 상태 확인
claude mcp remove sequential-thinking -s user   # 등록한 scope를 정확히 지정해서 제거
```

## 방법 2. `~/.claude.json` 직접 편집 (`user` 범위)

`~/.claude.json`의 최상위 `mcpServers` 항목에 아래 내용을 추가합니다.

```json
"mcpServers": {
  "sequential-thinking": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
    "env": {}
  }
}
```

기존에 다른 MCP가 있다면 항목을 이어서 추가합니다.

```json
"mcpServers": {
  "context7": {
    "type": "http",
    "url": "https://mcp.context7.com/mcp"
  },
  "sequential-thinking": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
    "env": {}
  }
}
```

> `~/.claude.json`에는 개인 설정, 세션 캐시, 그리고 다른 프로젝트의 `local` scope MCP 설정까지 함께 들어있는 큰 파일입니다. `mcpServers`(글로벌)와 `projects["<경로>"].mcpServers`(로컬)를 헷갈리지 않도록 주의하고, 직접 편집할 때는 JSON 문법 오류가 나지 않게 특히 조심합니다.

## 방법 3. `.mcp.json` (`project` 범위)

프로젝트 루트에 `.mcp.json` 파일을 생성합니다. git에 커밋하면 팀원과 설정을 공유할 수 있습니다.

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

> 협업자가 이 파일이 포함된 프로젝트를 처음 열면, `.mcp.json`의 서버는 바로 연결되지 않고 `claude mcp list`에 `⏸ Pending approval`로 표시됩니다. Claude Code가 처음 실행될 때 승인 여부를 묻고, 승인해야 연결됩니다. 이 승인 이력을 초기화하려면 `claude mcp reset-project-choices`를 실행합니다.

## 적용

설정 파일 수정 후 Claude Code를 재시작하면 적용됩니다. 정상 연결됐는지는 `claude mcp list`로 확인합니다.
