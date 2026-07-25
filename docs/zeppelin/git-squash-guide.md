# Git 커밋 Squash 가이드

여러 개의 커밋을 하나로 합치는 방법.

---

## 언제 사용하나?

- 같은 JIRA 이슈에 대해 커밋이 여러 개로 나뉘어진 경우
- PR 제출 전 커밋을 정리할 때
- Apache 등 오픈소스 기여 시 "1 이슈 = 1 커밋" 원칙을 맞출 때

---

## 순서

### 1. 인터랙티브 리베이스 시작

합치려는 커밋 수만큼 숫자를 조정한다. (2개 합치기 예시)

```bash
git rebase -i HEAD~2
```

### 2. 에디터에서 squash 설정

에디터가 열리면 아래처럼 보인다:

```
pick a75d70a1c [ZEPPELIN-6528] Upgrade Apache Shiro from 1.13.0 to 2.0.6
pick bc3796349 [ZEPPELIN-6528] Fix ShiroException import for Shiro 2.x compatibility
```

첫 번째 줄은 `pick` 유지, 나머지 줄의 `pick`을 `squash`(또는 `s`)로 변경:

```
pick a75d70a1c [ZEPPELIN-6528] Upgrade Apache Shiro from 1.13.0 to 2.0.6
squash bc3796349 [ZEPPELIN-6528] Fix ShiroException import for Shiro 2.x compatibility
```

저장하고 닫기 (vim: `:wq`)

### 3. 커밋 메시지 편집

두 커밋 메시지가 합쳐진 편집 화면이 열린다:

```
# This is the 1st commit message:

[ZEPPELIN-6528] Upgrade Apache Shiro from 1.13.0 to 2.0.6

- bullet 1
- bullet 2

# This is the commit message #2:

[ZEPPELIN-6528] Fix ShiroException import for Shiro 2.x compatibility
```

아래처럼 하나의 메시지로 정리한다:
- 제목은 첫 번째 커밋 메시지 사용
- 두 번째 커밋 내용은 bullet 항목으로 추가
- `# This is the commit message #2:` 블록 전체 삭제

```
[ZEPPELIN-6528] Upgrade Apache Shiro from 1.13.0 to 2.0.6

- bullet 1
- bullet 2
- 두 번째 커밋에서 추가한 내용 bullet으로 작성
```

저장하고 닫기 (vim: `:wq`)

### 4. Force push

```bash
git push --force-with-lease origin <브랜치명>
```

`--force-with-lease`는 `--force`보다 안전하다. 원격에 내가 모르는 커밋이 있으면 push를 막아준다.

---

## 확인

PR 페이지에서 커밋이 1개로 줄어들었는지 확인한다.

---

## 참고: vim 기본 명령어

| 명령어 | 동작 |
|--------|------|
| `i` | 편집 모드 진입 |
| `Esc` | 편집 모드 종료 |
| `:wq` | 저장하고 닫기 |
| `:q!` | 저장하지 않고 닫기 |
