import org.apache.spark.SparkConf
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, SparkSession}

import java.nio.file.{Files, Paths}
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import scala.collection.mutable.ListBuffer

/**
 * eCommerce 플랫폼의 사용자 이벤트 데이터를 처리하는 클래스.
 *
 * 이 클래스는 주어진 시작 날짜와 종료 날짜를 기반으로 월별 데이터를 필터링하고,
 * Spark를 활용하여 데이터를 처리 및 저장하는 기능을 제공합니다.
 * 데이터는 KST(한국 표준시)로 변환된 후, 연도(year), 월(month), 일(day) 기준으로
 * 파티셔닝되어 Parquet 형식으로 저장됩니다.
 *
 * 주요 기능:
 * - 시작 날짜와 종료 날짜 사이의 월별 데이터 경로 생성.
 * - 파일 경로 유효성 확인 후 존재하는 데이터만 필터링.
 * - Spark 설정 초기화 및 데이터 읽기 작업 수행.
 * - UTC 타임존의 이벤트 데이터를 KST로 변환.
 * - 데이터를 연도, 월, 일 기준으로 파티셔닝하여 저장.
 *
 * @param args 명령줄 인자로 전달된 값을 처리합니다. 기본적으로는 사용되지 않습니다.
 *
 * @throws DateTimeParseException 시작 날짜 또는 종료 날짜가 잘못된 형식("yyyy-MM-dd")으로 제공될 경우 예외가 발생할 수 있습니다.
 */
object EcommerceEventProcessor {
  /**
   * eCommerce 플랫폼의 사용자 이벤트 데이터를 처리하는 메인 메서드.
   *
   * 주어진 시작 날짜와 종료 날짜를 기반으로 월별 데이터를 필터링한 후, Spark를 사용해 데이터를 처리 및 저장합니다.
   * 이 메서드는 다음 단계를 포함합니다:
   *
   * 1. 시작 날짜와 종료 날짜를 기반으로 월별 데이터 경로를 생성합니다.
   * 2. 생성된 데이터 경로에서 실제로 존재하는 파일만 필터링합니다.
   * 3. Spark 설정을 초기화하고 Spark 세션을 생성합니다.
   * 4. 사용자 이벤트 데이터를 읽어오기 위해 스키마를 정의하고, CSV 파일 데이터를 읽어옵니다.
   * 5. UTC로 저장된 이벤트 시간을 KST(한국 표준시)로 변환합니다.
   * 6. 변환된 데이터에 연도(year), 월(month), 일(day) 정보를 추가하여 파티셔닝 컬럼을 생성합니다.
   * 7. 데이터를 Parquet 형식으로 저장하며, 연도, 월, 일 기준으로 파티셔닝합니다.
   *
   * 입력 데이터는 "src/main/resources/<yyyy-MMM>.csv.gz" 경로에 위치하며, 결과 데이터는
   * "src/main/resources/ecommerce_events" 디렉토리에 Parquet 형식으로 저장됩니다.
   *
   * @param args 명령줄 인자. 현재 이 메서드에서는 사용하지 않습니다.
   *
   * @throws DateTimeParseException 시작 날짜 또는 종료 날짜가 "yyyy-MM-dd" 형식이 아닐 경우 예외가 발생합니다.
   */
  def main(args: Array[String]): Unit = {
    val startDate = "2019-10-01"
    val endDate = "2019-11-01"

    val readPath = "src/main/resources"
    val readFormat = "csv.gz"
    val writePath = "src/main/resources/ecommerce_events"

    val monthlyData = generateMonthlyData(startDate, endDate)
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
      .withColumn("day", format_string("%02d", dayofmonth(col("event_time_kst"))))

    dfWithPartitionColumns.write
      .partitionBy("year", "month", "day")
      .mode("overwrite")
      .parquet(writePath)
  }

  /**
   * 주어진 시작 날짜와 종료 날짜 사이의 월을 "yyyy-MMM" 형식으로 생성하는 함수.
   *
   * 이 함수는 "yyyy-MM-dd" 형식의 시작 날짜와 종료 날짜를 입력받아, 범위 내의 월을 나타내는 문자열 리스트를 반환합니다.
   * 반환되는 각 문자열은 "yyyy-MMM" 형식("예: 2023-Jan")으로 포맷팅됩니다.
   * 시작 날짜와 종료 날짜의 월도 결과에 포함됩니다.
   *
   * @param startDate 시작 날짜로, "yyyy-MM-dd" 형식의 문자열.
   *                  이 날짜의 년도와 월이 범위의 시작을 정의합니다.
   * @param endDate   종료 날짜로, "yyyy-MM-dd" 형식의 문자열.
   *                  이 날짜의 년도와 월이 범위의 끝을 정의합니다.
   * @return 시작 월부터 종료 월까지의 범위 내 모든 월을 나타내는 문자열 리스트.
   *         각 문자열은 "yyyy-MMM" 형식으로 포맷됩니다.
   * @example
   * {{{
   * val result = generateMonthlyData("2023-01-15", "2023-03-10")
   * println(result) // 출력: List("2023-Jan", "2023-Feb", "2023-Mar")
   * }}}
   * @throws DateTimeParseException 입력된 startDate 또는 endDate가 "yyyy-MM-dd" 형식이 아닐 경우 예외를 발생시킵니다.
   */
  private def generateMonthlyData(startDate: String, endDate: String): List[String] = {
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
    val outputFormatter = DateTimeFormatter.ofPattern("yyyy-MMM", java.util.Locale.ENGLISH) // "yyyy-MMM" 형식
    val start = LocalDate.parse(startDate, formatter).withDayOfMonth(1)
    val end = LocalDate.parse(endDate, formatter).withDayOfMonth(1)

    val result = ListBuffer[String]()
    var current = start

    while (!current.isAfter(end)) {
      result += current.format(outputFormatter)
      current = current.plusMonths(1)
    }

    result.toList
  }
}
