# 1) 웹 크롤링을 통해 인기 뉴스 가져오기 
import requests
from bs4 import BeautifulSoup

response = requests.get("https://news.naver.com/main/officeList.naver") #html 소스 가져오기
html = response.text
soup = BeautifulSoup(html, 'html.parser') #파싱
content = soup.select(".list_tit") #인기 뉴스 링크, 제목, 내용

# 2) 뉴스 제목 필터링
titles = []
for article in content:
    titles.append(article.text.strip()) #제목만

import spacy
nlp = spacy.load("ko_core_news_sm") #한국어 전용 모델 로딩

keywords = []
for sentence in titles:
    nouns = nlp(sentence) #명사 추출 함수
    keywords.extend(token.text for token in nouns if token.pos_ == 'NOUN')
    #nouns : 명사가 담긴 리스트
    #token : nouns에서 꺼낸 개별 명사들
    #pos함수 : Part-Of-Speech, 품사를 말함

for n in reversed(keywords): #리스트를 역순으로 순회하여 삭제 작업 중 오류를 방지
    if (len(n) < 2):
        keywords.remove(n)
    elif ('.' in n):
        keywords.remove(n)

# 3) 필터링된 키워드로 검색(내용 구체화)
import urllib.request
import json

client_id = "Uy0VhciyOfTNUTQeMpCL"  #네이버 뉴스 API이용을 위한 ID와 PW
client_secret = "FFsldmkdrg"

keywords2 = keywords

for word in keywords:
    encText = urllib.parse.quote(word)  #검색할 단어(url 인코딩)
    encText2 = urllib.parse.quote("10") #찾을 검색 결과 수
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=" + encText2

    request = urllib.request.Request(url) #요청 전송
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request) #수신
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        response_dict = json.loads(response_body) # json형식으로 파싱 후 명사 추출
        for i in response_dict["items"]:
            nouns = nlp(i["title"])
            keywords2.extend(token.text for token in nouns if token.pos_ == 'NOUN')
    else:
        print("Error Code:" + rescode)

for n in reversed(keywords2):
    if (len(n) < 2):
        keywords.remove(n)
    elif ('.' in n):
        keywords.remove(n)

# 4) 워드클라우드 생성
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#워드클라우드 모양을 위한 부가적인 것들
import numpy as np
from PIL import Image

result = ' '.join(keywords2)
image_mask = np.array(Image.open("DASOM.png"))

wordcloud = WordCloud(font_path = 'C:\\Windows\\Fonts\\malgun.ttf', background_color = "white", 
                      max_font_size = 100, mask = image_mask).generate(result)

plt.imshow(wordcloud, interpolation='bilinear') #bilinear로 보간 
plt.axis('off')
plt.show()
plt.savefig("뉴스 키워드 워드클라우드.png")

# <아쉬웠던 점>
# 2차적으로 키워드 검색을 할 때 결과 수를 늘려 많은 키워드를 찾아 서로의 관련성을 고려해 분류하는 것까지 해보고 싶었으나
# 키워드가 많다보니 네이버 API호출 제한이 걸려 구현하지 못함.
