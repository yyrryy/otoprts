from django.contrib import admin

# Register your models here.
from .models import Voiture, Produit, Categories
admin.site.register(Voiture)
admin.site.register(Produit)
admin.site.register(Categories)
