from django.conf.urls import patterns, url

urlpatterns = patterns('cart.views',
    url(r'^simple', 'simple'),
    url(r'^thanks', 'thanks'),
    url(r'^', 'index'),
)
