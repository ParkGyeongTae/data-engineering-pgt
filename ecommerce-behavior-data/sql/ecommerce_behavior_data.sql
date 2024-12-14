CREATE EXTERNAL TABLE `bronze`.`ecommerce_behavior_data`(
  `event_time` timestamp COMMENT '이벤트 발생 시간',
  `event_type` string COMMENT '이벤트 타입',
  `product_id` int COMMENT '상품 ID',
  `category_id` bigint COMMENT '카테고리 ID',
  `category_code` string COMMENT '카테고리 코드',
  `brand` string COMMENT '브랜드',
  `price` double COMMENT '가격',
  `user_id` int COMMENT '사용자 ID',
  `user_session` string COMMENT '사용자 세션')
COMMENT '[데이터플랫폼] 전자상거래 행동 데이터'
PARTITIONED BY (
  `year` string COMMENT '파티션 연도 yyyy',
  `month` string COMMENT '파티션 월 mm',
  `day` string COMMENT '파티션 일 dd')
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://__bucket_name__/ecommerce_behavior_data/parquet'
TBLPROPERTIES (
  'classification'='parquet'
)
;