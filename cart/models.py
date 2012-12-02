from django.db import models
from catalog.models import Product

# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class OrderItem(models.Model):
    name = models.CharField(max_length=255)
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    price = models.IntegerField()
    count = models.IntegerField()

    def __unicode__(self):
        return self.name