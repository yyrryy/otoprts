from email.policy import default
from itertools import product
from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Voiture(models.Model):
    marque=models.CharField(max_length=50)
    
    date=models.IntegerField()

    model=models.CharField(max_length=50)

    carburant=models.CharField(max_length=50)
    def __str__(self) -> str:
        return f'{self.date}-{self.marque} {self.model} {self.carburant}'

class Categories(models.Model):
    title=models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.title

class Produit(models.Model):
    #title
    nom=models.CharField(max_length=100)

    #price
    prix= models.FloatField()

    #stock
    stock=models.IntegerField(default=1)	

    #brand
    marque=models.CharField(max_length=50, null=True)

    #country
    pays=models.CharField(max_length=50, null=True)

    #ref
    ref=models.CharField(max_length=50)

    #image
    image = CloudinaryField('image', folder='autoparts/', default=None, null=True)

    #cartgrise
    n_chasis=models.CharField(max_length=50, null=True)

    Categorie=models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)




class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    adress = models.CharField(max_length=500)
  
    # to save the data
    def register(self):
        self.save()
  
    @staticmethod
    def isExists(username):
        if Customer.objects.filter(username=username):
            return True
        return False


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
    product= models.ForeignKey(Produit, on_delete=models.CASCADE)
    amount=models.IntegerField(default=0)
    # name will be a string
    name=models.CharField(max_length=50)
    # email will be a string and not requuired
    email=models.EmailField(max_length=50, default=None, null=True)
    phone=models.IntegerField()
    adress=models.CharField(max_length=500)

    isconfirmed=models.BooleanField(default=False)
    isdelivered = models.BooleanField(default=False)


class Orderscostumer(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    product= models.ForeignKey(Produit, on_delete=models.CASCADE)
    # customer column
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount=models.IntegerField(default=0)
    # name will be a string
    name=models.CharField(max_length=50)
    # email will be a string and not requuired
    email=models.EmailField(max_length=50, default=None, null=True)
    phone=models.IntegerField()
    adress=models.CharField(max_length=500)

    isconfirmed=models.BooleanField(default=False)
    isdelivered = models.BooleanField(default=False)

