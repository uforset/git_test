from django.shortcuts import render

from django.http import HttpResponse

def main_page(request):
    return HttpResponse("메인페이지 확인")

# Create your views here.
