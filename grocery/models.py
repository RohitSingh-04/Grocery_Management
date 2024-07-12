# from django.db import models
from django.db import models

# Create your models here.
class Type(models.Model):
    typename = models.TextField(max_length=100 ,unique=True, null=False, blank=False)
    def __str__(self) -> str:
        return self.typename.capitalize()
    

class Product(models.Model):
    item_type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=60)
    price = models.FloatField(null=False, blank=False)
    quantity = models.IntegerField(default=1,null=False, blank=False)
    def __str__(self) -> str:
        return self.name

class Requests(models.Model):
    item_type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    comment = models.TextField(max_length=300)
    def __str__(self) -> str:
        return self.item_type.typename.capitalize()