# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys
import urllib.request
import json
import re
import csv

#가입해서 받은 client Id/ client secret 정보

client_id = "DfxlWzN1yptRVeE4qBuN"
client_secret = "McpQuTrwqV"

response = []
rescode =[]

movietable = list() # 영화 리스트를 담기위한 list

#csv 파일을 오픈하고 movietable list에 저장한다.
f = open("res_name.csv", 'r', encoding="UTF-8")

# /n 문자 제거
movietable = list(map(lambda x: x[:-1], f.readlines()))

print(movietable)

for_spark_movie_rating = list()
for_spark_movie_rating.append("Name"+','+"Rating")

movie_rating = list()

for movie_name in movietable:

  url = "https://openapi.naver.com/v1/search/movie.json?query=" + urllib.parse.quote(movie_name) # json 결과

  request = urllib.request.Request(url)#url의 정보를 가져와 request 클래스에 담음.
  request.add_header("X-Naver-Client-Id", client_id)#네이버 api header 값
  request.add_header("X-Naver-Client-Secret", client_secret)#네이버 api header 값
  
  res = urllib.request.urlopen(request)
  
  res_body = res.read()

  text_data = res_body.decode('utf-8')
  json_data = json.loads(text_data)

  rating = json_data['items'][0]['userRating']
  for_spark_movie_rating.append('"'+movie_name+'"'',' + rating)

  movie_rating.append([movie_name, rating])


print(for_spark_movie_rating)

# for spark
filecount = open("naver_raing_2.csv", "w", encoding="UTF-8")
for movie in for_spark_movie_rating:
    data = movie+"\n"
    filecount.write(data)
filecount.close()


f_res_name = open("res_rating.csv", "w", encoding="UTF-8")
movie_rating.sort(key = lambda x : x[1], reverse = True)
for movie_name in movie_rating:
    data = movie_name[0]+"\n"
    f_res_name.write(data)
f_res_name.close()