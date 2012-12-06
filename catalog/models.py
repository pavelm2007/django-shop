from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from autoslug import AutoSlugField

# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True)
    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


class Option(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name


class Product(models.Model):
    category = TreeForeignKey('Category', null=True, blank=False)
    option = TreeManyToManyField('Option')
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True)
    price = models.IntegerField()

    def __unicode__(self):
        return self.name

