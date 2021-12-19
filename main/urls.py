from django.shortcuts import render

# Create your views here.
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('loginregister', views.loginregister, name='loginregister'),
    
]