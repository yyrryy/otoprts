from django.shortcuts import render

# Create your views here.
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('byref', views.byref, name='by_ref'),
    path('bychas', views.bysach, name='by_chas'),
    path('coupon', views.coupon, name='coupon'),
    path('filters', views.filters, name='filters'),
    path('create', views.create, name='create'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('addbrand', views.addbrand, name='addbrand'),
    path('addmark', views.addmark, name='addmark'),
    path('addbulkfltrair', views.addbulkfltrair, name='addbulkfltrair'),
    path('addbulkfltrhuile', views.addbulkfltrhuile, name='addbulkfltrhuile'),
    path('addbulkrlmnt', views.addbulkrlmnt, name='addbulkrlmnt'),
    path('addbulkcroi', views.addbulkcroi, name='addbulkcroi'),
    path('addbulk/<int:ctg>', views.addbulk, name='addbulk'),
    path('commande', views.commande, name='commande'),
    path('orders', views.orders, name='orders'),
    path('orderitems/<int:id>', views.orderitems),
    path('dilevered/<int:id>', views.dilevered),

]