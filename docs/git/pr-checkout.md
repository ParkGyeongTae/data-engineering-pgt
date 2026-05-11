# PR 코드 로컬에서 테스트하기

다른 사람이 올린 PR의 코드를 로컬에서 테스트할 때 사용합니다.

## 방법 1. git fetch (기본)

```bash
# PR 번호로 로컬 브랜치 생성 후 checkout
git fetch origin pull/{PR번호}/head:{브랜치명}
git checkout {브랜치명}

# 예시: PR #42를 test-pr-42 브랜치로
git fetch origin pull/42/head:test-pr-42
git checkout test-pr-42
```

## 방법 2. GitHub CLI (간편)

```bash
gh pr checkout 42
```

## 정리

- 원본 PR에는 아무 영향 없음
- 테스트 후 브랜치를 삭제하면 깔끔하게 정리됨

```bash
git checkout main
git branch -d test-pr-42
```
