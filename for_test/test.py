from pyspark import SparkConf, SparkContext
 
conf = SparkConf().setMaster("local").setAppName("test")
sc = SparkContext(conf=conf) # spark context를 파이썬에서 사용하기 위함이다.
 
lines =sc.textFile("./latest.md") # 최신 영화 검색결과를 불러온다.
rdd0=lines.flatMap(lambda x: x.split("최신영화")) # "최신영화" 로 스플릿해서 스플릿 될때마다 줄을 바꿔서 RDD(rdd0)를 만든다. (결과에 중괄호 x)
rdd1=lines.flatMap(lambda x: x.split("최신 영화")) # "최신 영화" 로 스플릿해서 스플릿 될때마다 줄을 바꿔서 RDD(rdd1)를 만든다.(결과에 중괄호 x)
 
print("rdd0.count() :", rdd0.count() )  # number of element 출력
print("rdd0.first() :", rdd0.first() ) # element의 첫번째 출력

print("rdd1.count() :", rdd1.count() ) 
print("rdd1.first() :", rdd1.first() )

rdd0.saveAsTextFile("rdd0") # rdd0 directory 에 RDD를 저장한다.
rdd1.saveAsTextFile("rdd1") # rdd1 directory 에 RDD를 저장한다.
 
