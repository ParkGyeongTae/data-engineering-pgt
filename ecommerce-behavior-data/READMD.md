# data-engineering-pgt/ecommerce-behavior-data
## 프로젝트 요약
### EcommerceBehaviorData.scala (배치용-월별)
1. 데이터는 월별로 존재함
2. start_date(이상), end_date(이하)를 입력받아 해당 기간동안의 월별 데이터를 조회
3. 해당 기간의 데이터가 없는 경우 제외하고, 해당 기간동안의 데이터를 조회
4. UTC 시간을 KST 시간으로 변경
5. 데이터를 KST 기준 연, 월, 일로 파티셔닝하여 저장
### RecoveryEcommerceBehaviorData.scala (재처리용-특정일)
1. 데이터는 월별로 존재함
2. start_date(이상), end_date(이하)를 입력받아 해당 기간동안의 일별 데이터를 조회
3. 데이터가 UTC로 저장돼 있으므로, 매달 1일의 경우 전달의 데이터를 포함해야 KST로 온전한 데이터 저장 가능
4. 해당 기간의 데이터가 없는 경우 제외하고, 해당 기간동안의 데이터를 조회
5. UTC 시간을 KST 시간으로 변경
6. 데이터를 KST 기준 연, 월, 일로 파티셔닝하여 저장

## 사전 준비
```bash
# scala 2.12 설치 및 환경변수 설정
brew install scala@2.12
vim ~/.zshrc
echo 'export PATH="/opt/homebrew/Cellar/scala@2.12/2.12.20/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# java 11 설치 및 환경변수 설정
brew install openjdk@11
vim ~/.zshrc
echo 'export PATH="/opt/homebrew/Cellar/openjdk@11/11.0.25/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# spark 3.5.3 설치 및 환경변수 설정
sudo mkdir /opt/spark
sudo wget https://archive.apache.org/dist/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz
sudo tar -xvf spark-3.5.3-bin-hadoop3.tgz
sudo mv spark-3.5.3-bin-hadoop3/ /opt/spark
echo 'export SPARK_HOME="/opt/spark"' >> ~/.zshrc
echo 'export PATH="/opt/spark/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# intellij 설치
# scala plugin 설치
# java sdk 설정
# scala sdk 설정
# build-sbt 설정: spark-core, spark-sql 추가 (scala 버전에 맞게)
# https://mvnrepository.com/artifact/org.apache.spark/spark-core
libraryDependencies += "org.apache.spark" %% "spark-core" % "3.5.3"
# https://mvnrepository.com/artifact/org.apache.spark/spark-sql
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.5.3" % "provided"
# intellij 실행/디버깅 구성 -> "providor 범위를 가진 종속성 추가" 

# 기준 데이터
# https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
```
