"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainpage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main_page),
    path('ttmainpage/',include('mainpage.urls',)),
    # path('ttsignup/',include('signup.urls',)),                                            #회원가입
    # path('ttuser/',include('user.urls',)),                                              #로그인
    # path('ttcorona_travel_crawling/',include('corona_travel_crawling.urls',)),            #코로나 관련 크롤링
    # path('ttcorona_travel_visualization/',include('corona_travel_visualization.urls',)),  #코로나 관련 시각화
    path('ttnaver_news_crawling/',include('naver_news_crawling.urls',)),                  #네이버 뉴스 크롤링
    # path('ttnaver_news_visualization/',include('naver_news_visualization.urls',)),        #네이버 뉴스 시각화
    # path('ttnotice_list/',include('notice_list.urls',)),                                  #공지사항
]
