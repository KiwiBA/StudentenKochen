from django.conf.urls import include, url
from django.contrib import admin
from home import views

urlpatterns = [     
    #start page
    url(r'^$', 'home.views.index'),   
    #admin page   
    url(r'^admin/', include(admin.site.urls)),
    #recipes page
    url(r'^recipes/', include('recipes.urls', namespace="recipes")),
    #register page
    url(r'register/$', 'user_auth.views.StudentRegistration'),
    #login page
    url(r'login/$', 'user_auth.views.LoginRequest'),
    #logout page
    url(r'logout/$', 'user_auth.views.LogoutRequest'),
    #start page
     url(r'profile/$', 'user_auth.views.Profile'),  
]