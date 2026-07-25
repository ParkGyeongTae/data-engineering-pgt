# claude-dashboard 설치 및 사용 가이드

Claude Code 터미널 하단 상태바에 모델 사용량, 비용, Rate Limit 등을 표시해주는 플러그인입니다. Codex, Gemini, z.ai 등 다른 AI CLI의 사용량도 함께 확인할 수 있습니다.

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
  "displayMode": "detailed",
  "theme": "default",
  "cache": {
    "ttlSeconds": 300
  }
}
```

새 컴퓨터에서 동일하게 재현하려면:

1. 위 [설치](#설치) 단계를 그대로 진행 (`/claude-dashboard:setup`까지 실행해 `settings.json`의 `statusLine`이 등록되도록 함)
2. `~/.claude/claude-dashboard.local.json`을 위 내용으로 덮어쓰기

> `settings.json`의 `statusLine.command`는 `.../claude-dashboard/<버전>/dist/index.js`처럼 설치된 플러그인 버전 경로를 직접 참조합니다. `claude-dashboard.local.json`만 복사하고 `setup`(또는 `update`)을 한 번도 실행하지 않으면 상태바 자체가 등록되지 않으니 주의하세요.

## 표시 모드

| 모드 | 줄 수 | 주요 표시 항목 |
|------|-------|---------------|
| `compact` | 1줄 | 모델, 컨텍스트, 비용, Rate Limit |
| `normal` | 2줄 | + 프로젝트 정보, 세션 시간, 소진율, Todo |
| `detailed` | 6줄 | + 토큰 상세, 캐시 히트율, 예상 비용 등 |

각 모드에 어떤 위젯이 표시되는지, 위젯을 직접 골라 배치하는 `custom` 모드는 [GitHub README](https://github.com/uppinote20/claude-dashboard#widgets)에 전체 목록이 정리되어 있습니다.

## 테마 / 구분자

`theme`은 `default`(기본, pastel) 외에 `minimal`, `catppuccin`, `catppuccinLatte`(라이트 터미널용), `dracula`, `gruvbox`, `nord`, `tokyoNight`, `solarized`를 지원합니다.

`separator`는 `pipe`(`│`, 기본) / `space` / `dot`(`·`) / `arrow`(`›`) 중 선택할 수 있습니다.

```
/claude-dashboard:setup                          # 대화형으로 표시 모드/언어/플랜/테마 순서로 질문
/claude-dashboard:setup normal ko max            # 직접 지정: [표시모드] [언어] [플랜]
```

## 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `/claude-dashboard:setup` | 표시 모드, 언어, 플랜, 테마 설정 |
| `/claude-dashboard:check-usage` | Claude/Codex/Gemini/z.ai 사용량 확인 및 여유 있는 CLI 추천 |
| `/claude-dashboard:setup-alias` | 터미널에서 `check-ai` 명령어 alias 등록 (등록 후 `check-ai`, `check-ai --json`) |
| `/claude-dashboard:update` | 플러그인 업데이트 |

> `/plugin update claude-dashboard`로 플러그인 버전을 올린 뒤에는 `/claude-dashboard:update`를 한 번 더 실행해야 `settings.json`의 statusLine 경로가 새 버전 디렉터리를 가리키도록 갱신됩니다.

## 트러블슈팅

**상태바가 표시되지 않을 때**
1. `/plugin list` 로 설치 여부 확인
2. Claude Code 재시작
3. `settings.json`에 statusLine 설정이 있는지, 경로가 실제 설치된 버전 디렉터리와 일치하는지 확인

**캐시 초기화**

캐시는 `~/.cache/claude-dashboard/`에 저장되며 1시간 후 자동 정리됩니다. 즉시 초기화하려면:

```bash
rm -rf ~/.cache/claude-dashboard/
```
