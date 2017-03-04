from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>\d+)/(?P<term>\d+)/(?P<week>\d+)/?$', views.index, name='index')
]