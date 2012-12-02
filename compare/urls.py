from django.conf.urls import patterns, url

urlpatterns = patterns('compare.views',
    url(r'^', 'index'),
)
