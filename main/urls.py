from django.shortcuts import render

# Create your views here.
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('proccess', views.proccess, name='proccess'),
    path('byref', views.byref, name='by_ref'),
    path('bychas', views.bysach, name='by_chas')
]