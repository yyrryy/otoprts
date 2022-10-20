from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.title+'-'+str(self.id)
class Brand(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name+'-'+str(self.id)
class Model(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name+'-'+str(self.id)
    
class Mark(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.name+'-'+str(self.id)



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

class Pairingcode(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()

# orders table
class Ordersguest(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    products=models.ManyToManyField(Produit, blank=True)
    # name will be a string
    name=models.CharField(max_length=50)
    # email will be a string and not requuired
    email=models.EmailField(max_length=50, default=None, null=True)
    phone=models.IntegerField()
    # city will be a string
    city=models.CharField(max_length=50)

    adress=models.CharField(max_length=500)
    # subtotal float column used to detect
    subtotal=models.FloatField(default=0)
    # total float column
    total=models.FloatField(default=0)

    isconfirmed=models.BooleanField(default=False)
    isdelivered = models.BooleanField(default=False)

    # order by date
    class Meta:
        ordering = ['-date']
    # return the name and phone
    def __str__(self) -> str:
        return f'{self.name} {self.phone}'
    def __init__(self, name, email, phone, adress, amount) -> None:
        self.name=name
        self.email=email
        self.phone=phone
        self.adress=adress
        self.amount=amount



    

    isconfirmed=models.BooleanField(default=False)
    isdelivered = models.BooleanField(default=False)

class Shippingfees(models.Model):
    city=models.CharField(max_length=20)
    shippingfee=models.FloatField()
    def __str__(self) -> str:
        return f'{self.city} - {self.shippingfee}'

