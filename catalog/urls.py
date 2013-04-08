from django.conf.urls import patterns, url
from django.contrib import sitemaps
from catalog.sitemap import ProductSitemap, CategorySitemap


urlpatterns = patterns('catalog.views',
    url(r'^$', 'index'),
    url(r'^(?P<category_slug>[\w-]+)$', 'category'),
    url(r'^(?P<product_slug>[\w-]+).html$', 'product')
)

sitemaps = {
    "categories": CategorySitemap,
    "products": ProductSitemap
}

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', 'catalog.views.robots'),
)
