from django.shortcuts import render


def store(request):
    return render(request, 'shop/shop.html')


def product(request, id):
    return render(request, 'shop/product.html')
