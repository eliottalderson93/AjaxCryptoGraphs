from django.conf.urls import url
from . import views           
#these urls serve up ajax data for bokeh graphs using calls to my own server/api
urlpatterns = [
    #serves up ajaxDataSource data in x, y dict format
    #time coin data
    #url(r'^$', print("you made it into ajax")),
    url(r'^time/(?P<x_key>\w+)/(?P<y_key>\w+)/?$', views.ajaxSource),
    url(r'^time/(?P<x_key>\w+)/(?P<y_key>\w+)/(?P<coinParam>\w+)/?$', views.ajaxSource),
    url(r'^time/(?P<x_key>\w+)/(?P<y_key>\w+)/(?P<coinParam>\w+)/(?P<beginParam>\w+)/(?P<endParam>\w+)?$', views.ajaxSource),
    #compare coin data
    url(r'^compare/(?P<x_key>\w+)/(?P<y_key>\w+)/(?P<coinParamOne>\w+)/(?P<coinParamTwo>\w+)/?$', views.doubleAjaxSource),
    url(r'^compare/(?P<x_key>\w+)/(?P<y_key>\w+)/(?P<coinParamOne>\w+)/(?P<coinParamTwo>\w+)/(?P<beginParam>\w+)/(?P<endParam>\w+)?$', views.doubleAjaxSource),
] # http://127.0.0.1:8000/ajax/compare/Price/Price/bitcoin/tether/
# http://127.0.0.1:8000/ajax/time/Time/Price/bitcoin/