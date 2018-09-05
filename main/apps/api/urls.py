from django.conf.urls import url
from . import views           
#these urls serve up api calls to the proxy server
urlpatterns = [
    url(r'^$', views.bitcoin),     # serves up all bitcoin data
    url(r'^(?P<coin>\w+)/?$', views.allCoin),       # serves up all $coin data
    url(r'^(?P<coin>\w+)/(?P<begin>\w+)/(?P<end>\w+)/?$',views.timeCoin),     #serves up $coin data from $begin to $end 
]