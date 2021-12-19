from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.store, name='shop'),
    path('product/<int:id>', views.product, name='product-page')
]
