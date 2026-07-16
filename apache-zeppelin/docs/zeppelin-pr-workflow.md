# Apache Zeppelin PR 워크플로우

## 전체 흐름

0. 사전 준비 (최초 1회)
1. JIRA 이슈 생성
2. 브랜치 생성 및 코드 수정
3. 로컬 검증
4. 커밋 & 푸시
5. PR 생성
6. 리뷰
7. 머지
8. JIRA 이슈 닫기

---

## 0. 사전 준비 (최초 1회)

```bash
# fork: GitHub에서 apache/zeppelin → ParkGyeongTae/zeppelin fork
git clone https://github.com/ParkGyeongTae/zeppelin.git
cd zeppelin
git remote add upstream git@github.com:apache/zeppelin.git
git remote -v
# origin   -> ParkGyeongTae/zeppelin (fetch/push)
# upstream -> apache/zeppelin (fetch/push)
```

머지(6단계)를 하려면 GitHub Personal Access Token을 발급해 환경변수로 등록해둔다.

```bash
export GITHUB_OAUTH_KEY=<personal access token>
```

---

## 1. JIRA 이슈 생성

https://issues.apache.org/jira/browse/ZEPPELIN 에서 이슈를 생성한다.

- 이슈 번호 형식: `ZEPPELIN-XXXX`
- 이 번호를 브랜치명, 커밋 메시지, PR 제목에 사용한다.

---

## 2. 브랜치 생성 및 코드 수정

```bash
git checkout master
git pull upstream master
git checkout -b ZEPPELIN-XXXX
```

코드를 수정한다.

---

## 3. 로컬 검증

푸시 전에 관련 모듈 테스트를 돌려 회귀를 확인한다.

```bash
./mvnw test -pl <module>
# 특정 테스트만: ./mvnw test -pl <module> -Dtest=<TestClass>
```

---

## 4. 커밋 & 푸시

```bash
git add <파일>
git commit -m "[ZEPPELIN-XXXX] 변경 내용 요약"
git push origin ZEPPELIN-XXXX
```

---

## 5. PR 생성

GitHub에서 `ParkGyeongTae/zeppelin` → `apache/zeppelin` 으로 PR을 생성한다.

- PR 제목 형식: `[ZEPPELIN-XXXX] 변경 내용 요약`
- base 브랜치: `master`

PR이 생성되면 **GitHub PR 번호**(JIRA 번호와 다름)를 확인해둔다.

```bash
# PR 번호 확인
gh pr list --search "ZEPPELIN-XXXX" --repo apache/zeppelin --state all
```

---

## 6. 리뷰

커미터의 리뷰를 기다린다. 요청 사항이 있으면 수정 후 같은 브랜치에 추가 커밋하거나 force push한다.

CI가 실패하면 아래로 원인을 구분한다.

```bash
gh pr view <PR번호> --repo apache/zeppelin --json statusCheckRollup
```

- PR이 건드리지 않은 모듈(예: spark/flink 테스트인데 변경은 influxdb)에서만 실패 → conda 타임아웃, selenium flaky 등 인프라성 실패일 가능성이 높음
- 같은 시점의 `master` 브랜치 워크플로우(`gh run list --repo apache/zeppelin --branch master`)에서 동일 잡이 성공했는지 대조해 flaky 여부를 확인한다
- 필요 시 실패한 잡만 재실행(rerun)한다

---

## 7. 머지

리뷰가 완료되면 포크 클론(origin = ParkGyeongTae/zeppelin) 에서 실행한다.

### 사전 확인

| 항목 | 확인 방법 |
|------|-----------|
| `GITHUB_OAUTH_KEY` 설정 여부 | `echo $GITHUB_OAUTH_KEY` |
| PR mergeable 여부 | `python3 dev/merge_pr.py --pr XXXX --push-remote upstream --dry-run` |

### dry-run 먼저 실행

```bash
python3 dev/merge_pr.py --pr <GitHub PR 번호> --push-remote upstream --dry-run
```

### 실제 머지

```bash
python3 dev/merge_pr.py --pr <GitHub PR 번호> --push-remote upstream
```

성공 시 출력 예시:
```
PR #5285 merged! (hash: f8f51809)
Commented on PR with merge summary.
```

### 브랜치 정리

```bash
git branch -d ZEPPELIN-XXXX
git push origin --delete ZEPPELIN-XXXX
```

---

## 8. JIRA 이슈 닫기

머지 후 JIRA 이슈를 수동으로 Resolved 처리한다.

- https://issues.apache.org/jira/browse/ZEPPELIN-XXXX 접속
- 상태를 `Resolved` 또는 `Closed`로 전환

> `--resolve-jira` 옵션은 JIRA transition 이름이 한국어(`이슈 해결하기`)로 표시될 경우 동작하지 않으므로 수동 처리한다.

---

## 주의사항

- `--push-remote`의 기본값은 `apache`이므로, 포크 클론에서는 반드시 `--push-remote upstream`을 지정한다.
- `--pr`에는 JIRA 번호가 아닌 **GitHub PR 번호**를 사용한다.
- 릴리즈 브랜치가 있을 경우 `--release-branches branch-0.XX`를 추가한다 (현재는 없음).
