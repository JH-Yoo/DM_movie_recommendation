import os
import sys
import urllib.request
import json
import re
import csv
import time
start = time.time()

#가입해서 받은 Naver API를 위한 client Id/ client secret 정보
client_id = "DfxlWzN1yptRVeE4qBuN"
client_secret = "McpQuTrwqV"

###
crawling_list = list() # 네이버 블로그 크롤링 정보 리스트
movietable = list() # 한국 영화 진흥원에서 가져온 최신영화 리스트
movie_rating = list() # 영화의 Rating 정보를 담기 위한 리스트

# Hyper params
default_count_ratio = 2.0 # Recommend Score 화제성 가중치
default_rating_ratio = 1.0 # Recommend Score 평점 가중치


# 크롤링한 네이버 블로그 들의 title의 txt 파일을 오픈하고 crawling list에 저장한다.
f = open("./data/movie_list.txt", 'r', encoding="UTF-8")
crawling_list = f.readlines()
f.close()

# 한국 영화 진흥원의 최신 영화 csv 파일을 오픈하고 movietable list에 저장한다.
f = open("./data/movieset.csv",'r')
rea = csv.reader(f)
for row in rea:
    movietable.append(row)
f.close

strring = ''
result = list()

for i in movietable : 
    strring = ''.join(i) # 밑에 fliter함수를 사용하기 위해 list를 string으로 바꿔주는것이다.
    data2 = list(filter(lambda x: strring in x, crawling_list))  # sub string 이 string 안에 있는지 확인 하고 있으면 해당 string을 모두 list에 저장한다.
    #print(len(data2)) # 영화 리스트 안에 있는 영화를 검색하면 
    if len(data2) > 0:
      result.append([strring, len(data2)])

# 화제성 Count로 소팅
result.sort(key = lambda x : x[1], reverse = True)

total_count = 0

for _, count in result:
  total_count += count

# Recommend Score 수식
def get_movie_recommend_score(rating, count, total_count):
  return (default_rating_ratio * float(rating)) * (1 + (default_count_ratio * count / total_count))

# 영화 Rating 가져오는 부분
for movie_name, count in result:
  url = "https://openapi.naver.com/v1/search/movie.json?query=" + urllib.parse.quote(movie_name) # json 결과

  request = urllib.request.Request(url)#url의 정보를 가져와 request 클래스에 담음.
  request.add_header("X-Naver-Client-Id", client_id)#네이버 api header 값
  request.add_header("X-Naver-Client-Secret", client_secret)#네이버 api header 값
  
  res = urllib.request.urlopen(request)
  
  res_body = res.read()

  text_data = res_body.decode('utf-8')
  json_data = json.loads(text_data)

  rating = json_data['items'][0]['userRating']

  movie_rating.append([movie_name, get_movie_recommend_score(rating, count, total_count)])

# 결과값 Score로 소팅하여 저장
f_res_name = open("./result/res_rating_recommend.csv", "w", encoding="UTF-8")
movie_rating.sort(key = lambda x : x[1], reverse = True)
for movie_name in movie_rating:
    data = movie_name[0]+"\n"
    f_res_name.write(data)
f_res_name.close()

print("Finish to get the recommend movie chart!")
for i, (name, score) in enumerate(movie_rating):
  print("%-2d" % i + " %s " % name + "%.2f" % score)