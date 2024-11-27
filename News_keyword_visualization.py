# 1) 웹 크롤링을 통해 인기 뉴스 가져오기 
import requests
from bs4 import BeautifulSoup

response = requests.get("https://news.naver.com/main/officeList.naver")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
content = soup.select(".list_tit")

# 2) 뉴스 제목 필터링
titles = []
for article in content:
    titles.append(article.text.strip())

import spacy #명사 추출용
nlp = spacy.load("ko_core_news_sm") #한국어 전용 모델 로딩

keywords = []
for sentence in titles:
    nouns = nlp(sentence)
    keywords.extend(token.text for token in nouns if token.pos_ == 'NOUN')
for n in reversed(keywords):
    if (len(n) < 2):
        keywords.remove(n)
    elif ('.' in n):
        keywords.remove(n)

# 3) 필터링된 키워드로 검색(내용 구체화)
import os
import sys
import urllib.request
import json

client_id = "Uy0VhciyOfTNUTQeMpCL"  #네이버 뉴스 API이용을 위한 ID와 PW
client_secret = "FFsldmkdrg"

keywords2 = keywords

for word in keywords:
    encText = urllib.parse.quote(word)  #검색할 단어
    encText2 = urllib.parse.quote("10") #사용할 검색 결과 수
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=" + encText2

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        response_dict = json.loads(response_body)

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
import numpy as np
from PIL import Image

result = ' '.join(keywords2)
image_mask = np.array(Image.open("DASOM.png"))

wordcloud = WordCloud(font_path = 'C:\\Windows\\Fonts\\malgun.ttf', background_color = "white", 
                      max_font_size = 100, mask = image_mask).generate(result)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
plt.savefig("뉴스 키워드 워드클라우드.png")