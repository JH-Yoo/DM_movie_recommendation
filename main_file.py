# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys
import urllib.request
import json
import re

#가입해서 받은 client Id/ client secret 정보

client_id = "DfxlWzN1yptRVeE4qBuN"
client_secret = "McpQuTrwqV"

# 크롤링 개수 조정
serach_count = 1000

start = ''
display = '&display=100' #100개 검색.
params={}
encText = urllib.parse.quote("영화")#검색하고자 하는 키워드
sort = '&date'

response = []
rescode =[]

for i in range(0,serach_count): #i 의 범위 조정하면 더 많이 크롤링 가능. 현재 1페이지~1001페이지 까지 크롤링.

    #1페이지부터 시작.
    start='&start=%d'%(i+1)

    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + start + display + sort  # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과

    request = urllib.request.Request(url)#url의 정보를 가져와 request 클래스에 담음.
    request.add_header("X-Naver-Client-Id",client_id)#네이버 api header 값
    request.add_header("X-Naver-Client-Secret",client_secret)#네이버 api header 값


    response.append(urllib.request.urlopen(request))#http.client.httpresponse 객체를 리턴

    rescode.append(response[i].getcode())#http status code 리턴
    print(i)

#1. 내용 전체 출력
'''
print("1. 내용 전체 출럭 ------------------------------------")

for j in range(0,10):
    if(rescode[j]==200):#200 정상호출
        response_body = response[j].read()
        print(response_body.decode('utf-8'))#utf-8형식으로 디코딩하여 출력
    else:
        print("Error Code:" + rescode[j])#에러 발생시 에러코드 출력
'''
print("2.제목만 출력 ---------------------------------------")

resultList=[] #이녀석이 최종 제목 스트링들이 담길 리스트입니다. 자료형 : string list

for j in range(0,serach_count):
    if(rescode[j]==200):#200 정상호출
        response_body = response[j].read()
        text_data=response_body.decode('utf-8')
        json_data=json.loads(text_data)


    for x in json_data['items']:
        result=re.sub('<.+?>','',x['title'],0,re.I|re.S) #title만 가져오기 위해 파싱
        resultList.append(result)


# file output
f= open("movie_list.md", "w", encoding="UTF-8")

print(resultList)
for movie in resultList:
    data = movie+"\n"
    f.write(data)

f.close()

print(len(resultList))
