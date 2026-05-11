# sequential-thinking MCP 설정 방법

단계적 사고가 필요한 복잡한 작업에서 Claude의 추론 능력을 보조하는 MCP입니다.

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

## 방법 2. `.mcp.json` (프로젝트별)

프로젝트 루트에 `.mcp.json` 파일을 생성합니다. 해당 프로젝트에서만 적용되며, git에 커밋하면 팀과 공유할 수 있습니다.

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

## 방법 3. CLI 명령어

터미널에서 직접 추가할 수 있습니다.

```bash
# 글로벌 추가 (~/.claude.json에 저장)
claude mcp add sequential-thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking

# 프로젝트별 추가 (.mcp.json에 저장)
claude mcp add sequential-thinking -s project -- npx -y @modelcontextprotocol/server-sequential-thinking
```

## 적용

설정 파일 수정 후 Claude Code를 재시작하면 적용됩니다.
