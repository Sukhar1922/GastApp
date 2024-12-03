from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(req):
    return HttpResponse('<h1>Пиривет! У нас Периф</h1>')

def testPage(req):
    return HttpResponse('<h1>Пиривет! У нас Периф И теста</h1>')