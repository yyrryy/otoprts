from django.contrib import admin

# Register your models here.
# import models and register them
from .models import Customer, Orderscostumer

# register all models in the admin site
admin.site.register(Customer)
admin.site.register(Orderscostumer)
