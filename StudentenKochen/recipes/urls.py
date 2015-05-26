from django.conf.urls import url

from . import views

# /recipes/
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<recipe_id>\d+)/$', views.create, name='edit'),
]