# Claude Code MCP 설정 가이드

MCP(Model Context Protocol)는 Claude Code에 외부 도구나 데이터 소스를 연결하는 방법입니다.

## 설정 파일 위치

MCP는 `~/.claude.json` 파일의 `mcpServers` 항목에 등록합니다. 이 설정은 모든 프로젝트에 전역으로 적용됩니다.

```
~/.claude.json
```

## 현재 등록된 MCP

| 이름 | 용도 |
|------|------|
| `context7` | 라이브러리 공식 문서 실시간 조회 |
| `github` | GitHub 이슈, PR, 코드 검색 등 |

## MCP 추가 방법

`~/.claude.json`의 `mcpServers`에 항목을 추가합니다.

### HTTP 방식 (context7 예시)

```json
"mcpServers": {
  "context7": {
    "type": "http",
    "url": "https://mcp.context7.com/mcp"
  }
}
```

### stdio 방식 (npx로 실행하는 패키지)

```json
"mcpServers": {
  "my-mcp": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "패키지명"],
    "env": {}
  }
}
```

### 환경변수가 필요한 경우 (github 예시)

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

## 제거했던 MCP 재추가 방법

### sequential-thinking

단계적 사고가 필요한 복잡한 작업에 유용합니다. 아래 내용을 `mcpServers`에 추가하세요.

```json
"sequential-thinking": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
  "env": {}
}
```

## 적용

설정 파일 수정 후 Claude Code를 재시작하면 적용됩니다.

## 참고

- 공식 MCP 서버 목록: https://github.com/modelcontextprotocol/servers
- 프로젝트별로 MCP를 다르게 설정하려면 `~/.claude.json`의 `projects` 항목 안에 `mcpServers`를 추가하면 됩니다
