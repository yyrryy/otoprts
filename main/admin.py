from django.contrib import admin

# Register your models here.
from .models import Voiture, Produit, Categories, Coupon
admin.site.register(Voiture)
admin.site.register(Produit)
admin.site.register(Categories)
admin.site.register(Coupon)
