from django.conf.urls import url
from django.conf.urls.static import static

from foodosh import settings
from . import views

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^(?P<year>\d+)/(?P<term>\d+)/(?P<week>\d+)/?$', views.index, name='index'),

                  url(r'^ingredients$', views.ingredients_weeks, name='ingredients_weeks'),
                  url(r'^ingredients/(?P<year>\d+)/(?P<term>\d+)/(?P<week>\d+)/?$', views.shopping_list,
                      name='ingredients')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
