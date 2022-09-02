from django.contrib import admin

# Register your models here.
from .models import Voiture, Categories, Coupon, Ordersguest, Produit, Pairingcode, Shippingfees
admin.site.register(Voiture)
admin.site.register(Produit)
admin.site.register(Categories)
admin.site.register(Coupon)
# register all models in the admin site
admin.site.register(Ordersguest)
admin.site.register(Pairingcode)
admin.site.register(Shippingfees)

