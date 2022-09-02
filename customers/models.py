from django.db import models
# import Product from main.models
from main.models import Produit


# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    # password will be a string
    
    adress = models.CharField(max_length=500)
  
    # to save the data
    def register(self):
        self.save()
  
    @staticmethod
    def isExists(username):
        if Customer.objects.filter(username=username):
            return True
        return False

class Orderscostumer(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    products=models.ManyToManyField(Produit, blank=True)
    # customer column
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount=models.FloatField(default=0.00)
    # name will be a string