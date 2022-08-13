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

    
    
class Orders(models.Model):
    pdct=models.ForeignKey(Produit, on_delete=models.CASCADE)
    isconfirmed = models.BooleanField(default=False)
    isdelivered=models.BooleanField(default=False)
    # product well be one to many with order
    product=models.onetomany(Produit, on_delete=models.CASCADE)


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
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
  
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
  
        return False