from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin$', RedirectView.as_view(url='/admin/')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^imperavi/', include('imperavi.urls')),
                       url(r'^cart/', include('cart.urls')),
                       url(r'^compare/', include('compare.urls')),
                       url(r'^pricelist/', include('pricelist.urls')),
                       url(r'', include('catalog.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))
