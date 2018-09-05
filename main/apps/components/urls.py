from django.conf.urls import url
from . import views           
#these urls render the homepage html and ajax html components to the homepage to the page
urlpatterns = [
   #coin vs time
    url(r'^time/(?P<xkey>\w+)/(?P<ykey>\w+)?$',views.timePlot, name = "bitcoin"), #bokeh graph of all bitcoin data
    url(r'^time/(?P<xkey>\w+)/(?P<ykey>\w+)/(?P<coin>\w+)?$',views.timePlot, name = "anyCoin"), #bokeh graph of all $coin data
    url(r'^time/(?P<xkey>\w+)/(?P<ykey>\w+)/(?P<coin>\w+)/(?P<begin>\w+)/(?P<end>\w+)?$',views.timePlot, name = "rangeCoin"), #bokeh graph of $coin data from $begin to $end
    #coin vs coin
    url(r'^coin/(?P<xkey>\w+)/(?P<ykey>\w+)/(?P<coinX>\w+)/(?P<coinY>\w+)?$',views.compareCoinPlot, name = "twoCoin"), #bokeh graph of all $coinX vs $coinY data
    url(r'^coin/(?P<xkey>\w+)/(?P<ykey>\w+)/(?P<coinX>\w+)/(?P<coinY>\w+)/(?P<begin>\w+)/(?P<end>\w+)?$',views.compareCoinPlot, name = "twoRangeCoin"), #bokeh graph of $coinX vs $coinY data from $begin to $end
]