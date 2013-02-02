from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver

class CategoryManager(models.Manager):
    def get_query_set(self):
        return super(CategoryManager, self).get_query_set().exclude(hidden=True).exclude(count_products=0)


class ProductManager(models.Manager):
    def get_query_set(self):
        return super(ProductManager, self).get_query_set().exclude(is_active=False)


# Create your models here.
class Category(MPTTModel):
    CATEGORY_TYPES = (
        ('P', 'Products'),
        ('S', 'Sub categories'),
        )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True,
        help_text='Unique value for product page URL, created from name.')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    description = models.TextField(default="", blank=True)
    hidden = models.BooleanField(default=False)
    view = models.CharField(max_length=1, choices=CATEGORY_TYPES, default="P")
    count_products = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, default="",
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, default="",
        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # managers
    objects = models.Manager()
    active = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

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
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True)
    intro = models.TextField(default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to="product/", null=True, blank=True)
    option = TreeManyToManyField('Option', blank=True)
    SKU = models.CharField(max_length=64, default="", blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)

    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, default="", blank=True,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, default="", blank=True,
        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # managers
    objects = models.Manager()
    active = ProductManager()

    def __unicode__(self):
        return self.name

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def get_absolute_url(self):
        return reverse('catalog.views.product', args=[str(self.slug)])


class ProductMedia(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to="product/", null=True, blank=True)
    description = models.CharField(default="", blank=True, max_length=255)


# SIGNALS
@receiver(pre_save, sender=Product)
def counters_hook(sender, instance, **kwargs):
    try:
        old_category = sender.objects.get(pk=instance.pk).category
        new_category = instance.category

        if old_category != new_category:
            for ancestor in old_category.get_ancestors(include_self=True):
                ancestor.count_products -= 1
                ancestor.save()

            for ancestor in new_category.get_ancestors(include_self=True):
                ancestor.count_products += 1
                ancestor.save()

    except sender.DoesNotExist:
        for ancestor in instance.category.get_ancestors(include_self=True):
            ancestor.count_products += 1
            ancestor.save()


