from django.urls import path

from . import views

urlpatterns=[
    path('', views.blog, name='blog'),
    path('post', views.post, name='post')
]