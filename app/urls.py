from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.rates, name='index'),
    url(r'^rates/$', views.rates, name='rates'),
]
