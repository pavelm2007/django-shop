from django.conf.urls import patterns, url

urlpatterns = patterns('catalog.views',
    url(r'^$', 'index'),
    url(r'^(?P<category_slug>[\w-]+)$', 'category'),
    url(r'^(?P<product_slug>[\w-]+).html$', 'product')
)
