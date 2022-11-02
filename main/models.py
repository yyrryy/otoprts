from email.policy import default
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.title
class Brand(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name
class Model(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name
    
class Mark(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name



class Produit(models.Model):
    name=models.CharField(max_length=500, null=True)
    #price
    price= models.FloatField()

    #stock
    # stock=models.IntegerField(default=1)	



    #ref
    ref=models.CharField(max_length=50)

    #image
    # image = CloudinaryField('image', folder='autoparts/', default=None, null=True)

    #cartgrise
    # n_chasis=models.CharField(max_length=50, null=True)

    category=models.ForeignKey(Category,on_delete=models.CASCADE, default=None)
    brand=models.CharField(max_length=25, default=None)
    model=models.CharField(max_length=25, default=None)
    mark=models.CharField(max_length=25, default=None)
    def __str__(self) -> str:
        return f'{self.category} {self.brand}'
# cupppon codes table
class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()

class Client(models.Model):
    name=models.CharField(max_length=200)
    city=models.CharField(max_length=200, null=True, default=None)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name+'-'+str(self.city)

class Represent(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name




# orders table
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # name will be a string
    # email will be a string and not requuired

    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    isdelivered = models.BooleanField(default=False)

    # order by date
    class Meta:
        ordering = ['-date']
    # return the name and phone
    def __str__(self) -> str:
        return f'{self.id} {self.client}'


class Orderitem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    ref=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()



class Shippingfees(models.Model):
    city=models.CharField(max_length=20)
    shippingfee=models.FloatField()
    def __str__(self) -> str:
        return f'{self.city} - {self.shippingfee}'




class Pairingcode(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()
