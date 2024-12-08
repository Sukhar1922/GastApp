from django.shortcuts import render
from django.http import HttpResponse

TABELS = []

# Create your views here.

def index(req):
    return render(req, 'main/index.html')

def testPage(req):
    return HttpResponse('<h1>Пиривет! У нас Периф И теста</h1>')