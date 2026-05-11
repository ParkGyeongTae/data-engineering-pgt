# claude-dashboard 설치 및 사용 가이드

Claude Code 터미널 하단 상태바에 모델 사용량, 비용, Rate Limit 등을 표시해주는 플러그인입니다.

- GitHub: https://github.com/uppinote20/claude-dashboard
- 버전 기준: v1.26.1

## 사전 요구사항

- Claude Code v1.0.80 이상
- Node.js 18 이상

## 설치

Claude Code 내에서 아래 명령어를 순서대로 실행합니다.

```
/plugin marketplace add uppinote20/claude-dashboard
/plugin install claude-dashboard
/claude-dashboard:setup
```

setup 실행 시 대화형으로 언어, 플랜, 표시 모드를 선택하거나 아래처럼 직접 지정할 수 있습니다.

```
/claude-dashboard:setup normal ko max
```

## 나의 현재 설정

`~/.claude/claude-dashboard.local.json`

```json
{
  "language": "ko",
  "plan": "max",
  "displayMode": "normal",
  "theme": "default",
  "cache": {
    "ttlSeconds": 300
  }
}
```

새 컴퓨터에서 동일하게 재현하려면 설치 후 위 파일을 그대로 생성하면 됩니다.

## 표시 모드

| 모드 | 줄 수 | 주요 표시 항목 |
|------|-------|---------------|
| `compact` | 1줄 | 모델, 컨텍스트, 비용, Rate Limit |
| `normal` | 2줄 | + 프로젝트 정보, 세션 시간, 소진율, Todo |
| `detailed` | 6줄 | + 토큰 상세, 캐시 히트율, 예상 비용 등 |

## 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `/claude-dashboard:setup` | 표시 모드, 언어, 플랜 설정 |
| `/claude-dashboard:check-usage` | Claude/Codex/Gemini 전체 사용량 확인 |
| `/claude-dashboard:setup-alias` | 터미널에서 `check-ai` 명령어 alias 등록 |
| `/claude-dashboard:update` | 플러그인 업데이트 |

## 트러블슈팅

**상태바가 표시되지 않을 때**
1. `/plugin list` 로 설치 여부 확인
2. Claude Code 재시작
3. `settings.json`에 statusLine 설정이 있는지 확인

**캐시 초기화**

```bash
rm -rf ~/.cache/claude-dashboard/
```
