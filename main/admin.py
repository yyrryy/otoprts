from django.contrib import admin

# Register your models here.
from .models import Category, Coupon, Ordersguest, Produit, Pairingcode, Shippingfees, Brand, Model, Mark
admin.site.register(Brand)
admin.site.register(Produit)
admin.site.register(Category)
admin.site.register(Model)
admin.site.register(Coupon)
# register all models in the admin site
admin.site.register(Ordersguest)
admin.site.register(Pairingcode)
admin.site.register(Shippingfees)
admin.site.register(Mark)

