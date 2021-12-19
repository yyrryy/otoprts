from django.db import models

# Create your models here.


class Product(models.Model):
    #title
    title=models.CharField(max_length=100)

    #sku
    sku=models.CharField(max_length=20)

    #price
    price= models.FloatField()

    #stock
    stock=models.IntegerField(default=1)	

    #brand
    brand=models.CharField(max_length=50)

    #country
    country=models.CharField(max_length=50)

    #ref
    ref=models.CharField(max_length=50)

    
     

     
class Car(models.Model):
    caryr=models.IntegerField()

    carbrand=models.CharField(max_length=50)

    carmodel=models.CharField(max_length=50)

    careng=models.CharField(max_length=50)

    cartgrise=models.CharField(max_length=50)