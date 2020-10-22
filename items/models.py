from django.db import models
from django.core.validators import EmailValidator
# Create your models here.

class Item(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)

    Large = models.BooleanField(default = False)
    Medium = models.BooleanField(default = False)
    Small = models.BooleanField(default = False)
    

    Ldimension = models.CharField(max_length = 50)
    Mdimension = models.CharField(max_length = 50)
    Sdimension = models.CharField(max_length = 50)

    colour = models.CharField(max_length = 50)
    painted = models.BooleanField(default = False)  

    Lprice = models.IntegerField(default = None)
    Mprice = models.IntegerField(default = None)
    Sprice = models.IntegerField(default = None)

    Lstock = models.IntegerField(default = 10)
    Mstock = models.IntegerField(default = 10)
    Sstock = models.IntegerField(default = 10)

    lid = models.BooleanField(default = False)
    material = models.CharField(max_length = 50)
    description = models.TextField()

    def __str__(self):
        return self.id + " " + str(self.name) + " " + self.colour + " " + str(self.painted) + " " + self.material + " " + str(self.lid) + " " + self.description + " " + str(self.Large) + " " + str(self.Medium) + " " + str(self.Small) + " " + self.Lprice + " " + self.Mprice + " " + self.Sprice + " " + self.Lstock + " " + self.Mstock + " " + self.Sstock + " " + self.Ldimension + " " + self.Mdimension + " " + self.Sdimension

