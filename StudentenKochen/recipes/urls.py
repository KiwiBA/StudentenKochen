from django.conf.urls import url

from . import views

# /recipes/
urlpatterns = [
    url(r'^$', views.index, name='index'),
     # ex: /polls/5/
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
]