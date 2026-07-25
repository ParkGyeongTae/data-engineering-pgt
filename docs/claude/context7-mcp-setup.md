# context7 MCP 설정 방법

라이브러리, 프레임워크, SDK 등의 최신 공식 문서를 Claude가 실시간으로 조회할 수 있게 해주는 MCP입니다. `resolve-library-id`(라이브러리 이름 → Context7 ID 검색), `get-library-docs`(해당 ID의 최신 문서 조회) 두 가지 툴을 제공합니다.

- URL: `https://mcp.context7.com/mcp` (HTTP transport, 별도 설치 불필요)
- API 키 없이도 사용 가능하지만, [context7.com/dashboard](https://context7.com/dashboard)에서 무료 API 키를 발급받으면 더 높은 요청 한도를 받을 수 있습니다.

## 설정 범위(scope) 3가지

`claude mcp add`의 `-s/--scope` 옵션 기준으로 설정 범위가 3가지로 나뉩니다. 저장 위치와 공유 여부가 다르므로 용도에 맞게 선택합니다.

| 범위 | 적용 대상 | 저장 위치 | 다른 사람과 공유 |
|------|-----------|-----------|------------------|
| `local` (기본값) | 지금 이 프로젝트 디렉터리에서만 | `~/.claude.json` (`projects["<경로>"].mcpServers`) | ❌ 나만 |
| `user` | 모든 프로젝트 (글로벌) | `~/.claude.json` (최상위 `mcpServers`) | ❌ 나만 |
| `project` | 지금 이 프로젝트 | 프로젝트 루트 `.mcp.json` | ✅ git 커밋 시 팀과 공유 |

> `-s`를 생략하면 `local`이 기본값으로 적용됩니다. "글로벌로 설정한 줄 알았는데 다른 프로젝트에서 안 보인다"는 실수는 대부분 이 기본값 때문입니다.

---

## 방법 1. CLI 명령어 (권장)

```bash
# local: 이 프로젝트에서만, 나만 (scope 생략 시 기본값)
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# user: 모든 프로젝트에서, 나만 (글로벌)
claude mcp add --transport http context7 https://mcp.context7.com/mcp -s user

# project: 이 프로젝트, .mcp.json에 저장되어 팀과 공유
claude mcp add --transport http context7 https://mcp.context7.com/mcp -s project

# API 키를 사용해 요청 한도를 늘리고 싶은 경우 (원하는 scope에 --header 추가)
claude mcp add --transport http context7 https://mcp.context7.com/mcp -s user \
  --header "CONTEXT7_API_KEY: <발급받은 키>"
```

확인 및 삭제:

```bash
claude mcp list           # 등록된 MCP 서버와 연결 상태 확인
claude mcp get context7   # 특정 서버의 scope, 상태 확인
claude mcp remove context7 -s user   # 등록한 scope를 정확히 지정해서 제거
```

## 방법 2. `~/.claude.json` 직접 편집 (`user` 범위)

`~/.claude.json`의 최상위 `mcpServers` 항목에 아래 내용을 추가합니다.

```json
"mcpServers": {
  "context7": {
    "type": "http",
    "url": "https://mcp.context7.com/mcp"
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
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

> 협업자가 이 파일이 포함된 프로젝트를 처음 열면, `.mcp.json`의 서버는 바로 연결되지 않고 `claude mcp list`에 `⏸ Pending approval`로 표시됩니다. Claude Code가 처음 실행될 때 승인 여부를 묻고, 승인해야 연결됩니다. 이 승인 이력을 초기화하려면 `claude mcp reset-project-choices`를 실행합니다.

## 적용

설정 파일 수정 후 Claude Code를 재시작하면 적용됩니다. 정상 연결됐는지는 `claude mcp list`로 확인합니다.
