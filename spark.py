from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType 
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import col,array_contains
from pyspark.sql import SQLContext
import time
start = time.time()


conf = SparkConf().setMaster("local").setAppName("spark")
sc = SparkContext(conf=conf) # spark context를 파이썬에서 사용하기 위함이다.
sqlContext = SQLContext(sc) # spark sqlContext를 파이썬에서 사용하기 위함이다.

# spark를 파이썬에서 사용하기 위함이다.
spark = SparkSession.builder \
    .master("local") \
    .appName("spark") \
    .getOrCreate()

list = spark.read.option("header", "true").csv("./data/movielist.csv") # 영화 목록 csv를 불러온다.
list.show(list.count())
naverCount = spark.read.option("header", "true").csv("./data/naver_count.csv") # 크롤링의 결과를 카운트한 csv를 불러온다.
naverCount.show(naverCount.count())
rdd = list.join(naverCount, list["Title"] == naverCount["Name"],"inner").drop("Name").rdd #두개의 dataframe을 합치고 rdd로 만든다.
df = sqlContext.createDataFrame(rdd, ['Title', 'Genre','Director','Count']) # rdd를 dataframe으로 만든다.
df.coalesce(1).write.format('com.databricks.spark.csv').options(header='true').save('./result')# result directory make
print("time :", time.time() - start) 