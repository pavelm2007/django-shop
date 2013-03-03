# coding=utf-8
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail
from django.utils.translation import ugettext as _


class CategoryManager(models.Manager):
    def get_query_set(self):
        return super(CategoryManager, self).get_query_set().exclude(is_active=False)


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
    image = models.ImageField(upload_to="product/", null=True, blank=True, max_length=255)
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

    def thumbnail(self, width=64, height=64):
        if self.image:
            thumbnail = get_thumbnail(self.image, str(width) + 'x' + str(height))
            img_resize_url = unicode(thumbnail.url)
            html = '<a style="height:%spx; display:block" class="image-picker" href="%s">' \
                   '<img src="%s" alt="%s" width="%s" height="%s" />' \
                   '</a>'
            return html % (height, self.image.url, img_resize_url, self.name, thumbnail.width, thumbnail.height)

        return '<img src="http://placehold.it/64x64" alt="False">'

    thumbnail.short_description = _('Thumbnail')
    thumbnail.allow_tags = True


class ProductMedia(models.Model):
    product = models.ForeignKey(Product)
    image = ImageField(upload_to="product/", null=True, blank=True)
    description = models.CharField(default="", blank=True, max_length=255)
    is_main = models.BooleanField(default=False)


class Carousel(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="", blank=True)
    image = ImageField(upload_to="carousel/", null=True, blank=True)
    category = TreeForeignKey('Category', null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    is_active = models.BooleanField(default=True)

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

# copy main image into the product object
# this signal is disabled during the import process
@receiver(post_save, sender=ProductMedia)
def product_image(sender, instance, **kwargs):
    if bool(instance.image) is False:
        instance.delete()
        return False

    if instance.is_main:
        # removing is_main flag from all images
        for product_image in instance.product.productmedia_set.all():
            if product_image.pk != instance.pk:
                product_image.is_main = False
                product_image.save()

        # making this image as main
        instance.product.image = instance.image
        instance.product.save()
    else:
        if instance.product.productmedia_set.count() == 1:
            instance.is_main = True
            # call this signal again
            instance.save()


@receiver(post_delete, sender=ProductMedia)
def product_image_delete(sender, instance, **kwargs):
    if instance.is_main:
        if instance.product.productmedia_set.exclude(image=None).count() > 0:
            product_image = instance.product.productmedia_set.exclude(image=None).all()[0]
            product_image.is_main = True
            product_image.save()
        else:
            instance.product.image = None
            instance.product.save()
