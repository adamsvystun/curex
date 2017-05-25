from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.rates, name='index'),
    url(r'^rates/$', views.rates, name='rates'),
    url(r'^table/$', views.rates, {"show_plot":False}, name='table'),
    url(r'^plot/$', views.rates, {"show_table":False}, name='plot'),
    url(r'^cache_clear/$', views.cache_clear, name='cache_clear'),
]
