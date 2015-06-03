from django.conf.urls import url

from . import views

# /recipes/
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<recipe_id>\d+)/$', views.edit, name='edit'),
    url(r'^rate/(?P<recipe_id>[0-9]+)/$', views.rate, name='rate'),
    url(r'^comment/(?P<recipe_id>\d+)/$', views.comment, name='comment'),
    url(r'^search/$', views.search, name='search'),
]