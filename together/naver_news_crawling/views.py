from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse



from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import time

#단어 분석을 위한 import
from konlpy.tag import Okt

class naver_crawling:
    def __init__(self):
        self.test_data = data_analysis()
        self.__page_number = 1
    def open_browser(self):
        self.driver = wd.Chrome(executable_path='./chromedriver.exe')
        main_url = 'https://news.naver.com/'
        self.driver.get(main_url)
        self.driver.find_element(By.CSS_SELECTOR, "ul.Nlnb_menu_list>li:nth-child(7)>a").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "div.cluster_more>a").click()
        time.sleep(2)
        self.head_crawling()
        self.crawling()


    def move_browser(self, page_number):
        txt = 'div#paging>a:nth-child('+str(page_number)+')'
        self.driver.find_element(By.CSS_SELECTOR, txt).click()
        time.sleep(1)
        self.crawling()

    def head_crawling(self):
        # 가장 맨위 headline 부분의 기사
        head_news = self.driver.find_elements(By.CSS_SELECTOR, "div._persist>div.cluster>div>div.cluster_body")
        for news1 in head_news:
            news_list = news1.find_elements(By.CSS_SELECTOR, 'ul>li')
            for news in news_list:
                title = news.find_element(By.CSS_SELECTOR, 'div.cluster_text>a').text
                url = news.find_element(By.CSS_SELECTOR, 'div.cluster_text>a').get_attribute('href')
                self.test_data.set_title(title)
                self.test_data.set_url(url)

    def crawling(self):
        #section_body 부분
        section_body_news = self.driver.find_elements(By.CSS_SELECTOR,'div#section_body>ul')
        for news1 in section_body_news:
            news_list = news1.find_elements(By.CSS_SELECTOR,'li')
            for news in news_list:
                title = news.find_element(By.CSS_SELECTOR,'dl>dt:nth-child(2)>a').text
                url = news.find_element(By.CSS_SELECTOR,'dl>dt:nth-child(2)>a').get_attribute('href')
                self.test_data.set_title(title)
                self.test_data.set_url(url)

        # for idx in set1:
        #     body = idx.find('div',class_='cluster_body').find('ul',class_='cluster_list').find_all('li')
        #     for i in body:
        #         tit = i.find('div',class_='cluster_text').find('a',class_='cluster_text_headline nclicks(cls_wor.clsart)').text
        #         url = i.find('div', class_='cluster_text').find('a',class_='cluster_text_headline nclicks(cls_wor.clsart)')["href"]
        #         print('이름 : ', tit)
        #         print('주소 : ', url)
        #         test_data.set_data(tit)
        #         test_data.set_data(url)
        if self.__page_number != 5:
            self.__page_number+=1
            self.move_browser(self.__page_number)
        else:
            self.driver.close()
            # key = input("국가 이름 : ")
            # c = 0
            # for idx in self.test_data.get_title():
            #     if key in idx:
            #         print(idx)
            #         c+=1
            # print('기사 갯수 : ', c)
            # self.test_data.Noun_count()


    def get_title_data(self):
        return self.test_data.get_title()
    def get_url_data(self):
        return self.test_data.get_url()

class data_analysis:
    __data = []
    __url = []
    __img= ''
    __title=[]
    __count_title = {}
    __returndata=[]
    okt = Okt()
    def set_data(self, data):
        self.__data.append(data)

    def set_title(self,data):
        self.__title.append(data)
    def set_url(self,data):
        self.__url.append(data)
    def print_data(self):
        return self.__returndata

    def get_title(self):
        return self.__title

    def get_url(self):
        return self.__url

    def Noun_count(self):
        for line in self.__title:
            malist = self.okt.pos(''.join(line))
            #print(malist)

            # 명사들을 수집해서 반복되는 명사 count 를 진행한다.
            for word in malist:
                if word[1] == 'Noun':
                    if not (word[0] in self.__count_title):
                        self.__count_title[word[0]] = 0
                    self.__count_title[word[0]] += 1
        keys = sorted(self.__count_title.items(), key=lambda x: x[1], reverse=True)

        self.country=[]
        for word, count in keys:
            if word in ['러시아','미국','중국','북한','우크라']:
                #print('{0}({1})'.format(word, count))
                for idx in self.__title:
                    if word in idx:
                        #print(idx)
                        text = idx+'<br>'
                        self.__returndata.append(text)

from .models import naver_news
def crawling(request):
    test = naver_crawling()
    test.open_browser()
    t = test.get_title_data()
    u = test.get_url_data()
    error_count = 0
    for i in range(len(t)):
        title = t[i]
        url = u[i]
        try:
            naver_news(NEWS_TITLE=title, NEWS_URL=url).save()
        except Exception as msg:
            error_count+=1
            continue

    return HttpResponse(f'에러 갯수 : {error_count}')
# Create your views here.
