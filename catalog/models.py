from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from autoslug import AutoSlugField

class CategoryManager(models.Manager):
    def get_query_set(self):
        return super(CategoryManager, self).get_query_set().exclude(hidden=True).exclude(count_products=0)


# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True)
    hidden = models.BooleanField(default=False)
    count_products = models.IntegerField(default=0)
    # managers
    object = models.Manager()
    active = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def is_active(self):
        return self.count_products > 0 and self.hidden is False
    is_active.boolean = True
    is_active.short_description = 'Active'

    def __unicode__(self):
        return self.name


class Option(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name


class Product(models.Model):
    category = TreeForeignKey('Category', null=True, blank=False)
    option = TreeManyToManyField('Option', blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    image = models.ImageField(upload_to="product/", null=True, blank=True)
    SKU = models.CharField(max_length=64, default="", blank=True)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True)
    hidden = models.BooleanField(default=False)
    price = models.IntegerField()

    def __unicode__(self):
        return self.name
