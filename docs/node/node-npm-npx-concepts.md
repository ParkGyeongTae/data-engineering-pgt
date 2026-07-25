# Node / npm / npx 개념 정리

---

## 1. node

**한 줄 정의**
node는 JavaScript를 브라우저 밖에서 실행할 수 있게 해주는 런타임이다.

**핵심 포인트**
- 원래 JavaScript는 브라우저 안에서만 동작하던 언어였다.
- Node.js 덕분에 터미널에서 `.js` 파일을 서버·컴퓨터에서 직접 실행할 수 있다.

**예시**
```bash
node app.js          # app.js 파일 실행
node                  # 대화형 콘솔(REPL) 진입
```

---

## 2. npm (Node Package Manager)

**한 줄 정의**
npm은 Node.js용 패키지 관리자다.

**핵심 포인트**
- 다른 사람이 만든 코드(패키지)를 설치·관리해준다.
- 설치한 패키지는 프로젝트 폴더의 `node_modules/`에 저장된다.
- 어떤 패키지가 필요한지는 `package.json`에 기록된다.

**예시**
```bash
npm install express   # express 패키지 설치
npm install           # package.json에 정의된 의존성 전체 설치
npm run build          # package.json의 scripts 항목 실행
```

---

## 3. npx

**한 줄 정의**
npx는 패키지를 설치하지 않고 임시로 실행해주는 도구다.

**핵심 포인트**
- 매번 전역 설치(`npm install -g`)할 필요 없이, 필요할 때만 다운받아 실행한다.
- 실행이 끝나면 프로젝트에 남기지 않는다 (캐시에만 남음).
- MCP 서버 연결처럼 1회성 실행에 자주 쓰인다. 예) `npx -y @some/mcp-server`

**예시**
```bash
npx create-react-app my-app   # 설치 없이 1회성 실행
```

---

## 4. 비유로 정리 (Python 생태계와 비교)

| Node.js 생태계 | Python 생태계 (이 레포 기준) |
|---|---|
| `node` (런타임) | `python` |
| `npm` (패키지 관리자) | `uv` |
| `package.json` | `pyproject.toml` |
| `node_modules/` | `.venv/` |
| `npx` (임시 실행) | `uvx` |

---

## 5. 확인 질문

1. `node`, `npm`, `npx`는 각각 무엇을 하는 도구인가?
2. `npm install`과 `npx <패키지>`의 차이는?
3. `brew install node`를 한 번 실행하면 왜 세 명령어가 모두 사용 가능해지는가?
4. `node_modules/`와 `package.json`은 각각 무엇을 담고 있는가?
5. Python의 `uv`가 npm과 비슷한 이유는?

---

## 참고

- 설치/업그레이드 방법은 [node-installation.md](node-installation.md) 참고
