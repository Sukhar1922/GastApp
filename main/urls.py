from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.addPage),
    path('test', views.testPage),
]
