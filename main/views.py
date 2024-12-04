from django.shortcuts import render
from django.http import HttpResponse

from django.db import connection

# Create your views here.

def index(req):
    return HttpResponse('<h1>Пиривет! У нас Периф</h1>')

def testPage(req):
    return render(req, 'main/test.html')