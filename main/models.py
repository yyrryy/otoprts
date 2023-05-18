from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=150)
    code=models.CharField(max_length=150, default=None, null=True)
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
    image=models.CharField(max_length=500, default='/static/images/mark.jpg', null=True, blank=True)
    def __str__(self) -> str:
        return self.name



class Produit(models.Model):
    name=models.CharField(max_length=500, null=True)
    #price
    price= models.FloatField()

    #stock
    # stock=models.IntegerField(default=1)
    stock=models.BooleanField(default=True)


    #ref
    ref=models.CharField(max_length=50)

    #image
    image = models.CharField(max_length=500, default='/static/images/default.jpg', null=True, blank=True)
    mark=models.ForeignKey(Mark, on_delete=models.CASCADE, default=None, null=True, blank=True)
    #cartgrise
    # n_chasis=models.CharField(max_length=50, null=True)
    min=models.CharField(max_length=500, default=None, null=True, blank=True)
    isoffer=models.BooleanField(default=False)
    offre=models.CharField(max_length=500, default=None, null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE, default=None)
    # brand=models.CharField(max_length=25, default=None)
    # model=models.CharField(max_length=25, default=None)
    # mark=models.CharField(max_length=25, default=None)
    def __str__(self) -> str:
        return self.ref
# cupppon codes table
class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
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
    code=models.CharField(max_length=50, null=True, default=None)
    # name will be a string
    # email will be a string and not requuired
    salseman=models.CharField(max_length=50, null=True, default=None)
    modpymnt=models.CharField(max_length=50, null=True, default=None)
    modlvrsn=models.CharField(max_length=50, null=True, default=None)
    total=models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    # totalremise will be there i ncase pymny is cash
    totalremise=models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    isdelivered = models.BooleanField(default=False)
    ispaied = models.BooleanField(default=False)
    clientname=models.CharField(max_length=500, null=True, default=None)
    clientphone=models.CharField(max_length=500, null=True, default=None)
    clientaddress=models.CharField(max_length=500, null=True, default=None)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True)
    # order by date
    class Meta:
        ordering = ['-date']
    # return the name and phone

    # methode to determine wether it's delivered or not

    def __str__(self) -> str:
        return f'{self.id} {self.client}'


class Orderitem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()



class Shippingfees(models.Model):
    city=models.CharField(max_length=20)
    shippingfee=models.FloatField()
    def __str__(self) -> str:
        return f'{self.city} - {self.shippingfee}'




class Pairingcode(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()
