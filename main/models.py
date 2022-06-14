from django.db import models

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
    # image = models.ImageField()

    #cartgrise
    n_chasis=models.CharField(max_length=50, null=True)

    Categorie=models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)


    
     

 