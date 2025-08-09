CREATE EXTERNAL TABLE `bronze`.`ecommerce_behavior_data`(
  `event_time` timestamp COMMENT '이벤트가 발생한 시간 (UTC 기준)',
  `event_type` string COMMENT '한 가지 종류의 이벤트만 포함됨: 구매(purchase)',
  `product_id` int COMMENT '상품 ID',
  `category_id` bigint COMMENT '상품의 카테고리 ID',
  `category_code` string COMMENT '상품의 카테고리 분류 코드(가능한 경우). 주로 의미 있는 카테고리에 존재하며, 다양한 액세서리 종류에서는 생략됨',
  `brand` string COMMENT '소문자로 표시된 브랜드 이름 문자열, 생략될 수 있음',
  `price` double COMMENT '상품의 가격(float), 반드시 포함됨',
  `user_id` int COMMENT '영구 사용자 ID',
  `user_session` string COMMENT '임시 사용자 세션 ID. 각 사용자 세션마다 동일하며, 사용자가 긴 시간 동안 온라인 스토어에 다시 접속할 때마다 변경됨',
  `event_time_kst` timestamp COMMENT '이벤트가 발생한 시간 (KST 기준)')
COMMENT '[데이터플랫폼] 전자상거래 행동 데이터, 다중 카테고리 온라인 스토어에서 수집된 사용자와 제품 간의 이벤트 데이터를 포함한 전자상거래 행동 데이터'
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
  's3://___your_bucket_name___/ecommerce_behavior_data/parquet'
TBLPROPERTIES (
  'classification'='parquet'
)
;