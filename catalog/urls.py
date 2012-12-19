from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('catalog.views',
    url(r'^$', 'index'),
    url(r'^(?P<category_slug>[\w-]+)$', 'category'),
    url(r'^(?P<product_slug>[\w-]+).html$', 'product')
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
