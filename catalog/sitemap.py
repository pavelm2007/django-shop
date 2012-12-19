from django.contrib.sitemaps import Sitemap
from catalog.models import Product, Category
from django.contrib.sitemaps import Sitemap

class ProductSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Product.objects.filter()

    def lastmod(self, obj):
        return ''

    # changefreq can be callable too
    def changefreq(self, obj):
        return "weekly"

    def location(self, obj):
        return '/' + obj.slug + '.html'

class CategorySitemap(Sitemap):
    priority = 0.7

    def items(self):
        return Category.objects.filter()

    def lastmod(self, obj):
        return ''

    # changefreq can be callable too
    def changefreq(self, obj):
        return "daily"

    def location(self, obj):
        return '/' + obj.slug
