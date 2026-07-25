# ACP(Agent Client Protocol)란?

---

## 1. 한 줄 정의

ACP는 **코드 에디터(Client)**와 **AI 코딩 에이전트(Agent)**가 서로 통신하는 방식을 표준화한 오픈 프로토콜이다. Zed Industries가 2025년 8월에 공개했고, 이후 JetBrains 등이 합류해 여러 에디터·에이전트가 함께 채택하는 표준으로 발전하고 있다.

---

## 2. 왜 필요한가 (배경)

- Claude Code, Gemini CLI 같은 AI 코딩 에이전트가 늘어나면서, 에디터마다 "이 에이전트는 이렇게 붙이고, 저 에이전트는 저렇게 붙여야" 하는 **1:1 커스텀 연동**이 반복적으로 필요해졌다.
- 에디터 입장에서는 지원하는 에이전트 수만큼 통합 코드를 새로 짜야 하고, 에이전트 개발자 입장에서도 지원하려는 에디터마다 다른 API에 맞춰야 했다.
- ACP는 이 문제를 **LSP(Language Server Protocol)가 언어 서버 연동을 표준화한 방식과 동일한 아이디어**로 푼다. 에디터와 에이전트가 각각 ACP 하나만 구현하면, ACP를 지원하는 모든 에디터 ↔ 모든 에이전트 조합이 커스텀 코드 없이 바로 연결된다.

---

## 3. 구조 (Client - Agent)

```
┌──────────────────────────┐        stdio + JSON-RPC 2.0        ┌──────────────────────────┐
│  Client (에디터)          │ ───────────────────────────────▶  │  Agent (AI 코딩 에이전트)   │
│  Zed, JetBrains IDE,      │ ◀───────────────────────────────  │  Claude Code, Gemini CLI  │
│  Neovim, Emacs 등         │      (하위 프로세스로 실행)          │  등                        │
└──────────────────────────┘                                    └──────────────────────────┘
```

- **Client**: 사용자가 실제로 여는 에디터. 세션을 시작하고, 에이전트를 하위 프로세스로 실행(spawn)하며, 파일 읽기/쓰기·터미널 실행 같은 요청을 승인/거절하는 주체.
- **Agent**: ACP를 구현한 AI 코딩 에이전트. 사용자의 프롬프트를 받아 코드를 분석·수정하고, 필요한 작업(파일 수정, 명령 실행 등)을 Client에게 요청한다.
- MCP의 Host-Client-Server 구조와 달리, ACP는 **에디터가 먼저 손을 뻗어 에이전트를 실행·통제하는 방향**이 뚜렷하다. 즉 "에디터가 클라이언트, 에이전트가 서비스 제공자"라는 비대칭 구조다.

---

## 4. 동작 흐름 (세션 라이프사이클)

1. **initialize** — Client와 Agent가 처음 연결되면 서로의 구현 정보(버전, 지원 기능)를 교환하는 핸드셰이크.
2. **session/new** — Client가 새 대화 세션을 생성 요청.
3. **session/prompt** — 사용자의 요청(프롬프트)을 Agent에게 전달.
4. **session/update** — Agent가 진행 상황(응답 스트리밍, 파일 diff, 작업 로그 등)을 Client에게 실시간으로 알리는 알림(notification).
5. **tool call 보고** — Agent가 수행한/수행하려는 작업을 표준화된 형태로 Client에 보고.
6. **session/request_permission** — 파일 수정, 명령 실행처럼 위험할 수 있는 작업 전에 Agent가 Client(=사용자)에게 승인을 요청.

이 흐름 덕분에 에디터는 에이전트가 지금 뭘 하고 있는지(어떤 파일을 고치는지, 어떤 명령을 실행하려는지)를 항상 UI로 보여주고, 위험한 작업은 사용자 승인 없이 실행되지 않도록 제어할 수 있다.

---

## 5. 전송 방식

| 방식 | 설명 | 상태 |
|---|---|---|
| **stdio + JSON-RPC 2.0** | 에디터가 에이전트를 하위 프로세스로 실행하고, 표준입출력으로 JSON-RPC 메시지를 주고받음 | 표준, 현재 주로 사용되는 방식 |
| **HTTP/WebSocket (원격 에이전트)** | 로컬 프로세스가 아니라 클라우드 등 별도 인프라에서 도는 에이전트와 연결 | 초안/작업 중(work-in-progress) |

MCP의 `stdio` transport와 개념은 비슷하지만, ACP는 "에디터가 에이전트 프로세스를 직접 띄운다"는 로컬 실행 모델이 기본값이라는 점이 특징이다.

---

## 6. MCP와의 관계 — 헷갈리지 않게 구분하기

이름과 구조가 비슷해서 혼동하기 쉽지만, **둘은 겹치는 프로토콜이 아니라 서로 다른 방향을 표준화한다.**

| | MCP (Model Context Protocol) | ACP (Agent Client Protocol) |
|---|---|---|
| 표준화 대상 | LLM/에이전트가 **도구·데이터**에 접근하는 방식 | 에디터가 **에이전트**를 실행·제어하는 방식 |
| 비유 | USB-C (기기 ↔ 액세서리) | LSP (에디터 ↔ 언어 서버) |
| 방향 | 에이전트 → 외부 리소스(Tools/Resources) | 에디터(Client) → 에이전트(Agent) |
| 예시 | context7, github MCP 서버 연동 ([mcp-concepts.md](mcp-concepts.md)) | Zed/JetBrains에서 Claude Code, Gemini CLI 실행 |

두 프로토콜은 상호보완적으로 함께 쓰인다. ACP 스펙은 가능한 경우 **MCP의 JSON 표현을 그대로 재사용**하고, ACP 세션이 시작될 때 에디터가 자신이 연결해둔 MCP 서버 목록을 에이전트에게 넘겨줄 수 있다. 즉, "에디터 ↔ 에이전트"는 ACP로, "에이전트 ↔ 도구/데이터"는 MCP로 각각 담당하는 구조다.

---

## 7. 비유로 정리

ACP는 **AI 코딩 에이전트를 위한 LSP**라고 이해하면 된다.

- LSP 이전: 에디터마다 언어별로 커스텀 자동완성/진단 플러그인을 따로 만들어야 했음.
- LSP 이후: 언어 서버 하나만 구현하면 LSP를 지원하는 모든 에디터에서 그대로 동작.
- ACP 이전: 에디터마다 지원하려는 AI 에이전트별로 커스텀 통합이 필요.
- ACP 이후: 에이전트 하나가 ACP만 구현하면, ACP를 지원하는 모든 에디터(Zed, JetBrains, Neovim 등)에서 바로 실행 가능.

---

## 8. 채택 현황

- **Zed**: ACP를 처음 공개하고 네이티브로 지원.
- **JetBrains**: 2025년 10월 Zed와 파트너십을 맺고 IntelliJ IDEA, PyCharm, WebStorm에 네이티브 ACP 지원 추가. 이후 두 회사가 함께 [ACP Registry](https://agentclientprotocol.com/registry)를 운영.
- **Neovim, Emacs, VS Code**: 커뮤니티 플러그인 형태로 지원.
- **에이전트 쪽**: Claude Code, Gemini CLI 등 다수의 CLI 기반 코딩 에이전트가 ACP를 구현.

---

## 9. 확인 질문

1. ACP에서 Client와 Agent는 각각 무엇을 가리키며, 누가 누구를 실행하는가?
2. `session/request_permission`은 왜 필요한가? 이게 없으면 어떤 문제가 생길까?
3. ACP와 MCP는 같은 문제를 푸는 프로토콜인가? 아니라면 각각 무엇을 표준화하는가?
4. LSP와 ACP의 유사점은 무엇인가?

---

## 참고

- [Agent Client Protocol 공식 사이트 및 스펙](https://agentclientprotocol.com/)
- [Zed — Agent Client Protocol 소개](https://zed.dev/acp)
- [Zed Blog — The ACP Registry is Live](https://zed.dev/blog/acp-registry)
- [Reference Implementation (GitHub)](https://github.com/agentclientprotocol/agent-client-protocol)
- 이 레포의 MCP 개념 문서: [mcp-concepts.md](mcp-concepts.md)
