# from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Type(models.Model):
    typename = models.TextField(max_length=100 ,unique=True, null=False, blank=False)
    def __str__(self) -> str:
        return self.typename.capitalize()
    

class Product(models.Model):
    item_type = models.ForeignKey(Type,null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=60, unique=True)
    price = models.FloatField(null=False, blank=False)
    quantity = models.IntegerField(default=1,null=False, blank=False)
    def __str__(self) -> str:
        return self.name

class Requests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.ForeignKey(Type,null=True, on_delete=models.SET_NULL)
    comment = models.TextField(max_length=300)
    def __str__(self) -> str:
        return self.item_type.typename.capitalize()
