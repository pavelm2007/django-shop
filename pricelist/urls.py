from django.conf.urls import patterns, url

urlpatterns = patterns('pricelist.views',
    url(r'^yml.xml$', 'yml'),
)