import org.apache.spark.SparkConf
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, SparkSession}

import java.nio.file.{Files, Paths}
import java.time.{LocalDate, ZoneOffset}
import java.time.format.DateTimeFormatter
import scala.collection.mutable.ListBuffer

/**
 * RecoveryEcommerceEventProcessor
 *
 * 이 클래스는 eCommerce 플랫폼의 사용자 이벤트 데이터를 처리하는 프로그램입니다.
 * 사용자 이벤트 데이터를 읽고, 처리하며, 결과를 KST(한국 표준시)로 변환하여 Parquet 형식으로 저장합니다.
 * 데이터는 Spark를 활용해 일별 데이터를 처리하며, 연도(year), 월(month), 일(day) 기준으로 파티셔닝되어 저장됩니다.
 *
 * 주요 기능:
 * - 주어진 시작 날짜와 종료 날짜를 기반으로 데이터 파일 경로를 생성합니다.
 * - 해당 파일 경로 중 존재하는 파일만 필터링합니다.
 * - Spark 설정을 초기화하고 데이터 읽기 및 변환 작업을 수행합니다.
 * - UTC 기준 이벤트 시간을 KST로 변환합니다.
 * - 데이터를 연도, 월, 일 기준으로 파티셔닝하여 Parquet 형식으로 저장합니다.
 *
 * @throws DateTimeParseException 시작 날짜 또는 종료 날짜가 "yyyy-MM-dd" 형식이 아닐 경우 발생합니다.
 * @throws java.nio.file.NoSuchFileException 파일 경로가 유효하지 않을 경우 발생할 수 있습니다.
 */
object RecoveryEcommerceEventProcessor {

  /**
   * eCommerce 플랫폼의 사용자 이벤트 데이터를 처리하는 메인 메서드.
   *
   * 이 메서드는 시작 날짜와 종료 날짜를 기반으로 데이터를 필터링하고,
   * Spark를 사용해 데이터를 처리 및 저장합니다. 결과는 KST(한국 표준시)로 변환된 데이터를
   * 연도(year), 월(month), 일(day) 기준으로 파티셔닝하여 Parquet 형식으로 저장합니다.
   *
   * 주요 단계:
   * 1. 시작 날짜와 종료 날짜를 입력받아 일별 데이터를 생성합니다.
   * 2. 생성된 데이터를 "src/main/resources/<날짜>.csv.gz" 형식의 파일 경로로 변환합니다.
   * 3. 해당 파일이 존재하는 경로만 필터링합니다.
   * 4. Spark 설정을 초기화하고, 사용자 이벤트 데이터를 읽어옵니다.
   * 5. UTC 기준 이벤트 시간을 KST로 변환합니다.
   * 6. 변환된 데이터를 연도, 월, 일 기준으로 파티셔닝하여 Parquet 형식으로 저장합니다.
   *
   * @param args 명령줄 인자를 처리하지만, 현재는 사용되지 않습니다.
   *
   * @throws DateTimeParseException 시작 날짜 또는 종료 날짜가 "yyyy-MM-dd" 형식이 아닐 경우 발생합니다.
   * @throws java.nio.file.NoSuchFileException 파일 경로가 유효하지 않을 경우 발생할 수 있습니다.
   */
  def main(args: Array[String]): Unit = {
    val start_date = "2019-11-01"
    val end_date = "2019-11-01"

    val readPath = "src/main/resources"
    val readFormat = "csv.gz"
    val writePath = "src/main/resources/ecommerce_events"

    val monthlyData = generateDailyData(start_date, end_date).distinct
    val updatedMonthlyData = monthlyData.map(date => s"$readPath/$date.$readFormat")
    val filteredMonthlyData = updatedMonthlyData.filter(path => Files.exists(Paths.get(path)))

    val conf = new SparkConf()
      .setMaster("local[*]")
      .setAppName("User Event Processor")
      .set("spark.app.description", "Processes user event data from an eCommerce platform")
      .set("spark.sql.session.timeZone", "UTC")
      .set("spark.driver.memory", "2g")
      .set("spark.executor.memory", "2g")
      .set("spark.memory.fraction", "0.8")
      .set("spark.memory.storageFraction", "0.3")
    val spark = SparkSession.builder().config(conf).getOrCreate()

    val schema = StructType(Array(
      StructField("event_time", TimestampType, nullable = true),
      StructField("event_type", StringType, nullable = true),
      StructField("product_id", IntegerType, nullable = true),
      StructField("category_id", LongType, nullable = true),
      StructField("category_code", StringType, nullable = true),
      StructField("brand", StringType, nullable = true),
      StructField("price", DoubleType, nullable = true),
      StructField("user_id", IntegerType, nullable = true),
      StructField("user_session", StringType, nullable = true)
    ))

    val df: DataFrame = spark.read
      .option("header", "true")
      .option("delimiter", ",")
      .schema(schema)
      .csv(filteredMonthlyData: _*)

    val dfWithKST: DataFrame = df.withColumn("event_time_kst", from_utc_timestamp(col("event_time"), "Asia/Seoul"))

    val dfWithPartitionColumns: DataFrame = dfWithKST
      .withColumn("year", year(col("event_time_kst")))
      .withColumn("month", month(col("event_time_kst")))
      .withColumn("day", dayofmonth(col("event_time_kst")))

    dfWithPartitionColumns.write
      .partitionBy("year", "month", "day")
      .mode("overwrite")
      .parquet(writePath)
  }

  /**
   * 주어진 시작 날짜와 종료 날짜 사이의 데이터를 하루 단위로 추출하는 함수.
   *
   * 이 함수는 시작 날짜와 종료 날짜를 기준으로, 매일 데이터를 생성합니다.
   * 각 날짜는 UTC 기준에서 9시간을 뺀 시간으로 조정됩니다. 결과는 "yyyy-MMM" 형식으로 반환됩니다.
   *
   * @param startDate 시작 날짜를 나타내는 문자열. "yyyy-MM-dd" 형식으로 제공되어야 합니다.
   * @param endDate 종료 날짜를 나타내는 문자열. "yyyy-MM-dd" 형식으로 제공되어야 합니다.
   * @return 시작 날짜와 종료 날짜 사이의 일별 데이터를 나타내는 문자열 리스트.
   *         각 날짜는 "yyyy-MMM" 형식으로 포맷됩니다.
   *
   * @throws DateTimeParseException 입력된 날짜가 "yyyy-MM-dd" 형식이 아닐 경우 예외를 발생시킵니다.
   */
  private def generateDailyData(startDate: String, endDate: String): List[String] = {
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
    val outputFormatter = DateTimeFormatter.ofPattern("yyyy-MMM", java.util.Locale.ENGLISH)
    val start = LocalDate.parse(startDate, formatter).atStartOfDay(ZoneOffset.UTC).minusHours(9)
    val end = LocalDate.parse(endDate, formatter).atStartOfDay(ZoneOffset.UTC).plusDays(1).minusHours(9)

    val result = ListBuffer[String]()
    var current = start

    while (!current.isAfter(end)) {
      result += current.format(outputFormatter)
      current = current.plusDays(1)
    }

    result.toList
  }
}
