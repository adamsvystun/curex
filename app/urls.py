from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.rates, name='index'),
    url(r'^rates/(?P<cur_from>\w+)/(?P<cur_to>\w+)/(?P<date_from>\w+)/(?P<date_to>\w+)/$', views.rates, name='rates'),
]
