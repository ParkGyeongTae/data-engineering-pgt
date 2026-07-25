# MCP(Model Context Protocol)란?

---

## 1. 한 줄 정의

MCP는 LLM 애플리케이션(Claude 등)이 외부 도구·데이터·서비스에 접근할 수 있도록 만든 **표준 프로토콜**이다. Anthropic이 만들었고 현재는 오픈 스탠다드로 공개되어 있다.

---

## 2. 왜 필요한가 (배경)

- LLM 자체는 학습 시점 이후의 정보나 사내 시스템, 실시간 데이터에 접근할 수 없다.
- MCP 이전에는 "Claude에 GitHub 연동", "Claude에 DB 연동"처럼 도구마다 각각 다른 방식의 커스텀 연동을 만들어야 했다.
- MCP는 이 연동 방식을 하나의 표준 프로토콜로 통일해서, **도구를 만드는 쪽**과 **도구를 쓰는 LLM 클라이언트**가 서로 각자 한 번만 구현하면 되게 만든다. (M개 도구 × N개 클라이언트 문제를 M+N 문제로 줄인다)

---

## 3. 구조 (Host - Client - Server)

```
┌─────────────────────────────────────┐
│  Host (Claude Code, Claude Desktop)  │
│  ┌─────────────┐                     │
│  │ MCP Client   │──1:1──▶ MCP Server A (예: context7)
│  ├─────────────┤                     │
│  │ MCP Client   │──1:1──▶ MCP Server B (예: github)
│  └─────────────┘                     │
└─────────────────────────────────────┘
```

- **Host**: 사용자가 실제로 쓰는 애플리케이션 (Claude Code, Claude Desktop 등). LLM과의 대화를 담당.
- **Client**: Host 내부에서 각 서버와 1:1로 연결을 관리하는 커넥터.
- **Server**: 실제로 도구/데이터를 제공하는 외부 프로그램 또는 서비스. 하나의 Host가 여러 Server에 동시에 연결될 수 있다.

---

## 4. 3가지 연결 방식 (Transport)

| Transport | 동작 방식 | 예시 |
|---|---|---|
| `stdio` | 로컬 프로세스를 실행해서 표준입출력으로 통신 | `sequential-thinking` (npx로 로컬 실행) |
| `http` | 원격 서버에 HTTP로 요청 | `context7` (`https://mcp.context7.com/mcp`) |
| `sse` | HTTP 기반 스트리밍 방식 (구버전, 최신 스펙에서는 `http`로 통합되는 추세) | - |

- `stdio`는 설치가 필요하고 내 컴퓨터에서 프로세스가 직접 돈다. (예: `npx -y @modelcontextprotocol/server-sequential-thinking`)
- `http`는 별도 설치 없이 URL만 등록하면 된다.

---

## 5. MCP가 제공하는 3가지 요소 (Primitives)

| 요소 | 설명 | 예시 |
|---|---|---|
| **Tools** | LLM이 호출할 수 있는 함수. 실행하면 부수효과(외부 API 호출 등)가 생길 수 있음 | `create_pull_request`, `resolve-library-id` |
| **Resources** | LLM이 읽을 수 있는 데이터(파일, DB 레코드 등). 함수 호출이 아니라 컨텍스트로 제공됨 | 특정 파일 내용, 이슈 목록 |
| **Prompts** | 서버가 미리 정의해둔 프롬프트 템플릿. 사용자가 재사용 가능 | "이 PR을 리뷰해줘" 같은 정형화된 요청 |

실무에서 가장 많이 쓰이는 건 **Tools**다. Claude Code에서 MCP 서버를 붙이면 대부분 이 Tools 목록이 늘어나는 것이라고 이해하면 된다.

---

## 6. 비유로 정리

MCP는 흔히 **USB-C**에 비유된다.

- USB-C 이전: 기기마다 다른 충전 단자 (5핀, 8핀, 마이크로 5핀 …) → 케이블도 제각각.
- USB-C 이후: 단자 하나로 노트북, 폰, 모니터 다 연결 가능.
- MCP 이전: LLM 앱마다, 도구마다 다른 연동 방식.
- MCP 이후: 서버 하나 만들면 Claude Code, Claude Desktop 등 MCP를 지원하는 모든 Host에서 그대로 사용 가능.

---

## 7. 이 레포에서 사용 중인 MCP 예시

실제 설정 방법은 각 문서에 정리되어 있다.

- [context7](../claude/context7-mcp-setup.md) — `http` transport, 라이브러리 최신 공식 문서 조회 (Tools 제공)
- [github](../claude/github-mcp-setup.md) — 이슈/PR 조회 및 생성 등 GitHub 작업 (Tools 제공)
- [sequential-thinking](../claude/sequential-thinking-mcp-setup.md) — `stdio` transport, 단계적 사고 프로세스를 위한 도구

세 서버 모두 `claude mcp list`로 연결 상태를 확인할 수 있고, 설정 범위(`local`/`user`/`project`)는 [context7 설정 문서](../claude/context7-mcp-setup.md#설정-범위scope-3가지)에 정리된 기준을 그대로 따른다.

---

## 8. 확인 질문

1. MCP에서 Host, Client, Server는 각각 무엇을 가리키는가?
2. `stdio`와 `http` transport의 차이는?
3. Tools와 Resources는 어떻게 다른가?
4. MCP가 없던 시절과 비교했을 때, MCP가 실제로 줄여주는 것은 무엇인가?

---

## 참고

- [Model Context Protocol 공식 사이트](https://modelcontextprotocol.io)
- 이 레포의 실제 MCP 설정 예시: [context7](../claude/context7-mcp-setup.md), [github](../claude/github-mcp-setup.md), [sequential-thinking](../claude/sequential-thinking-mcp-setup.md)
