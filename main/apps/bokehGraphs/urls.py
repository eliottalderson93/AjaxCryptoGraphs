from django.conf.urls import url
from . import views           
#these urls render the homepage html and ajax html components to the homepage to the page
urlpatterns = [
    #single coin bokeh graphs (or coin vs time)
    url(r'^$', views.graph), #renders single page app html
    #url(r'test^$', views.test),
]