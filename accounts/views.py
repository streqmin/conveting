from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

def index(request):
    return HttpResponse("Conveting accounts app page")
    

class Register(CreateView):
    '''
    회원가입 view
    '''

class Login(View):
    '''
    로그인 view
    '''

class Logout(View):
    '''
    로그아웃 view
    '''