from django.conf.urls import patterns, url

urlpatterns = patterns('catalog.views',
    url(r'^$', 'index'),
    url(r'^(?P<category_id>[\w-]+)$', 'category'),
    url(r'^(?P<product_id>[\w-]+).html$', 'product')
)
