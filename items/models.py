from django.db import models
from django.core.validators import EmailValidator
# Create your models here.

class Item(models.Model):
    username = models.CharField(max_length = 50)
    price = models.IntegerField()
    sizes = models.CharField(max_length = 50)
    dimensions = models.CharField(max_length = 50)
    colours = models.CharField(max_length = 50)

    def __str__(self):
        return self.username + " " + str(self.price) + " " + self.sizes + " " + self.dimensions + " " + self.colours

