from django.conf.urls import url

from . import views

# /recipes/
urlpatterns = [
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<recipe_id>\d+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<recipe_id>\d+)/$', views.delete, name='delete'),
    url(r'^rate/(?P<recipe_id>[0-9]+)/$', views.rate, name='rate'),
    url(r'^comment/(?P<recipe_id>\d+)/$', views.comment, name='comment'),
    url(r'^ownRecipes/$', views.ownRecipes, name='ownRecipes'),
    url(r'^search/$', views.search, name='search'),
    url(r'^extendedSearch/$', views.extendedSearch, name='extendedSearch'),
]