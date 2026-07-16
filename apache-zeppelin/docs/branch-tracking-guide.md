# upstream/master 추적 브랜치 설정 가이드

포크한 레포에서 `upstream/master`를 추적(tracking)하는 방법 두 가지. `git pull`, `git status`만으로 upstream 대비 최신 상태를 바로 확인할 수 있게 해준다.

전제: [zeppelin-pr-workflow.md](zeppelin-pr-workflow.md)의 0단계처럼 `upstream` 리모트가 등록되어 있어야 한다.

```bash
git remote -v
# origin   -> ParkGyeongTae/zeppelin (fetch/push)
# upstream -> apache/zeppelin (fetch/push)
```

---

## 방법 1: 기존 `master` 브랜치가 `upstream/master`를 추적하도록 변경

포크의 `master`를 origin이 아니라 upstream 기준으로 관리하고 싶을 때 사용한다.

```bash
git checkout master
git fetch upstream
git branch --set-upstream-to=upstream/master master
git pull
```

확인:

```bash
git branch -vv
# master  xxxxxxx [upstream/master] ...
```

> 이후 `git push`를 실행하면 기본적으로 `upstream`으로 push를 시도하게 된다. 실수로 upstream에 직접 push하지 않도록 `git push origin master`처럼 리모트를 명시하거나, push는 아래 `git config`로 별도 제한해두는 것이 안전하다.
>
> ```bash
> git config branch.master.pushRemote origin
> ```

---

## 방법 2: `upstream-master`라는 새 브랜치를 만들어 `upstream/master`를 추적

기존 `master`(origin 추적, PR 브랜치 생성 기준)는 그대로 두고, upstream 최신 상태 확인·비교용 브랜치를 별도로 두고 싶을 때 사용한다. 이 레포에서 실제로 사용 중인 방식이다.

```bash
git fetch upstream
git checkout -b upstream-master upstream/master
```

확인:

```bash
git branch -vv
# upstream-master  xxxxxxx [upstream/master] ...
```

이후 최신화는 다음으로 충분하다.

```bash
git checkout upstream-master
git pull
```

---

## 두 방법 비교

| | 방법 1 | 방법 2 |
|---|---|---|
| 브랜치명 | `master` | `upstream-master` (신규) |
| 기존 `master`(origin 추적) | 대체됨 | 유지됨 |
| PR용 브랜치(`ZEPPELIN-XXXX`) 생성 기준 | `master`(=upstream) | 기존 `master`(origin) 그대로 사용 가능 |
| 실수로 upstream에 push할 위험 | 있음 (별도 설정 필요) | 없음 |

- 새 작업 브랜치는 최신 코드를 기준으로 만들어야 하므로, upstream과 동기화된 브랜치(`master` 또는 `upstream-master`)에서 분기한다.
- 방법 2가 origin/upstream 역할이 분리되어 있어 사고 위험이 적다. 이미 `master`가 origin을 추적 중인 상태에서 upstream 추적을 추가하고 싶다면 방법 2를 권장한다.
