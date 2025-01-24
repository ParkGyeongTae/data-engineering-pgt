## 도커 관련 명령어
```bash
# 도커 이미지 빌드
docker build -t ubuntu1804:0.0.1 .

# 도커 컨테이너 실행
docker run -i -t -d --name ubuntu1804 ubuntu1804:0.0.1

# 도커 컨테이너 접속
docker exec -it ubuntu1804 /bin/bash

# 도커 컨테이너 중지
docker stop ubuntu1804

# 도커 컨테이너 삭제
docker rm ubuntu1804

# 도커 이미지 삭제
docker rmi ubuntu1804:0.0.1
```
