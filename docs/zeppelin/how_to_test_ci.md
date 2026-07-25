# 포크에서 CI(GitHub Actions) 테스트하는 방법

Apache Zeppelin의 CI는 GitHub Actions로 돌아가고, 정의는 [`.github/workflows`](https://github.com/apache/zeppelin/tree/master/.github/workflows)에 있다. `apache/zeppelin`에 PR을 올리고 결과를 기다리는 대신, 내 포크(`ParkGyeongTae/zeppelin`)에서도 똑같은 워크플로우를 그대로 돌려볼 수 있다.

---

## 1. 포크에서 Actions 활성화

1. 내 포크 저장소로 이동 (`https://github.com/ParkGyeongTae/zeppelin`)
2. **Actions** 탭 클릭
3. **"I understand my workflows, go ahead and enable them"** 버튼 클릭

포크는 기본적으로 Actions가 꺼져 있어서, 포크당 최초 1회만 해주면 된다.

---

## 2. 실행 트리거

이 레포의 워크플로우들은 다음 조건에서 실행된다.

- `push`: `dependabot/**` 브랜치를 제외한 모든 브랜치
- `pull_request`: `master`, `branch-*` 대상

즉 브랜치를 포크에 push만 해도 자동으로 돈다.

```bash
git push origin ZEPPELIN-XXXX
```

이후 포크의 **Actions** 탭에서 실행 로그와 결과를 확인한다.

---

## 3. 어떤 워크플로우가 도는지

| 워크플로우 | 파일 | 하는 일 |
|---|---|---|
| `core` | `.github/workflows/core.yml` | `zeppelin-server`/`zeppelin-web` 빌드 + 핵심 모듈(`zeppelin-interpreter`, `zeppelin-server`) 테스트, 그리고 이 테스트에 필요한 일부 인터프리터(spark, shell, markdown) 포함 |
| `frontend` | `.github/workflows/frontend.yml` | 프론트엔드/e2e 테스트 |
| `quick` | `.github/workflows/quick.yml` | 빠른 검증: Apache RAT 라이선스 헤더 체크, `mvn validate` |
| `stale` | `.github/workflows/stale.yml` | 오래된 이슈/PR을 정리하는 봇 워크플로우 — 코드 변경과는 무관 |

특정 인터프리터나 모듈만 고쳤더라도 보통 `core`와 `quick`은 통과해야 한다. 워크플로우가 안 도는 것 같으면 각 파일의 `on.push` / `on.pull_request` 조건을 확인한다.

---

## 4. 비용

Public 레포이므로 GitHub Actions 사용은 무료다. 내 포크(public)에서 돌려도 과금되는 시간이 없다.

---

## 5. (선택) push 전에 로컬에서 먼저 확인하기

CI 시간을 아끼고 싶으면, push 하기 전에 워크플로우가 실행하는 것과 동일한 명령어를 로컬에서 먼저 돌려본다.

```bash
# 라이선스 헤더 체크 (quick 워크플로우와 동일)
./mvnw apache-rat:check -Prat

# maven validate (quick 워크플로우와 동일)
./mvnw validate -Pinclude-hadoop

# core 모듈 빌드 (core 워크플로우와 동일)
./mvnw install -Pbuild-distr -DskipTests -pl zeppelin-server,zeppelin-web,spark-submit,spark/scala-2.12,spark/scala-2.13,markdown,angular,shell -am -Pweb-classic -Phelium-dev -Pexamples
```

---

## 주의사항

- Actions는 포크마다 최초 1회 활성화해야 한다.
- 브랜치를 push하면 자동으로 트리거되므로 별도 명령이 필요 없다.
- 결과 확인은 항상 **내 포크**의 Actions 탭에서 한다 (`apache/zeppelin` 탭이 아님).
