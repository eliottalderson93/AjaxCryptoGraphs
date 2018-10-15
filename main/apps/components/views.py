from django.shortcuts import render, HttpResponse, redirect, render_to_response
import requests, json
import pandas as pd
import numpy as np
from django.template import loader
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models import HoverTool
from django.core.serializers.json import DjangoJSONEncoder
def timePlot(request,xkey,ykey,coin = False,begin = False, end = False):
    baseURL = "http://18.220.161.116/ajax/time/"
    baseName = "Bitcoin"
    ajaxRoute = baseURL + str(xkey) + "/" + str(ykey) + "/"
    if(coin):
        ajaxRoute += (str(coin) + "/")
        baseName = str(coin).capitalize()
    if(begin):
        ajaxRoute += (str(begin) + "/")
    if(end):
        ajaxRoute += str(end)
    #originally ajaxDataSource, now is a get route into a column data source. ajaxDataSource is good for real time data
    jsonDict = requests.get(ajaxRoute).json()
    #print("timePlot data from api:",jsonDict["x"][0],jsonDict["y"][0])
    nDays = 2
    df = pd.DataFrame({'x': pd.to_datetime(jsonDict["x"][::nDays],yearfirst = True), 'y' : jsonDict["y"][::nDays] , 'date' : jsonDict["x"][::nDays]})
    #df = df.fillna(0)
    #print("dataframe:\n",df)
    # print("dataframe x:\n",df['x'])
    # print("dataframe y:\n",df['y'])
    titleStr = baseName + " " + str(xkey) + " vs " + str(ykey)
    TOOLTIPS = [
        ("Date", "@date"),
        ("Price", "$@y{0,0.00}")
    ]
    FORMAT = { "Date" : "datetime" }
    plot = figure(x_axis_type="datetime", plot_width=1000, plot_height=700, x_axis_label = str(xkey), y_axis_label = str(ykey), title = titleStr)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    hover = HoverTool(tooltips=TOOLTIPS, mode = 'vline', formatters = FORMAT)
    plot.add_tools(hover)
    source = ColumnDataSource(df)
    #print("CDSx::",source.data['x'],"\nCDSy::",source.data['y'],"\nCDScols::",source.column_names)
    plot.line(x='x',y='y', source=source)
    #print("plot complete:",plot.select(dict(type=HoverTool))[0].tooltips)
    script, div = components(plot)
    context = {
        "script" : script,
        "div" : div
    }
    #print("context:", context)
    template = loader.get_template("bokehGraphs/ajaxGraph.html")
    return HttpResponse(template.render(context = context, request = request))
def compareCoinPlot(request,xkey,ykey,coinX = False, coinY = False,begin = False, end = False):
    print("you are in the compare component view")
    baseURL = "http://18.220.161.116/ajax/compare/"
    ajaxRoute = baseURL + str(xkey) + "/" + str(ykey) + "/"
    baseNameX = "doggo"
    baseNameY = "doggo"
    if(coinX):
        ajaxRoute += (str(coinX) + "/")
        baseNameX = str(coinX).capitalize()
    if(coinY):
        ajaxRoute += (str(coinY) + "/")
        baseNameY = str(coinY).capitalize()
    if(begin):
        ajaxRoute += (str(begin) + "/")
    if(end):
        ajaxRoute += str(end)
    #originally ajaxDataSource, now is a get route into a column data source. ajaxDataSource is good for real time data
    jsonArr = requests.get(ajaxRoute).json() # ["x"][0],jsonDict["y"][0]
    x, y, date = parseArr(jsonArr)
    df = pd.DataFrame({'x': x, 'y' : y , 'date' : date, 'xLabel' : jsonArr[0]['xName'],'yLabel' : jsonArr[0]['yName']})
    # df = df.fillna(0)
    # print("dataframe:\n",df)
    titleStr = baseNameX + " " + str(xkey) + " vs " + baseNameY + " " + str(ykey)
    TOOLTIPS = [
        ("Price " + baseNameX, "$@x{0,0.00}"),
        ("Price " + baseNameY, "$@y{0,0.00}"),
        ("Date" , "@date")
    ]
    FORMAT = {"Date" : "datetime"}
    plot = figure(plot_width=1000, plot_height=700, x_axis_label = str(xkey), y_axis_label = str(ykey), title = titleStr)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    hover = HoverTool(tooltips=TOOLTIPS, mode = 'vline', formatters = FORMAT)
    plot.add_tools(hover)
    source = ColumnDataSource(df)
    #print("CDSx::",source.data['x'],"\nCDSy::",source.data['y'],"\nCDScols::",source.column_names)
    plot.scatter(x='x',y='y', source=source)
    #print("plot complete:",plot.select(dict(type=HoverTool))[0].tooltips)
    script, div = components(plot)
    context = {
        "script" : script,
        "div" : div
    }
    #print("context:", context)
    template = loader.get_template("bokehGraphs/ajaxGraph.html")
    return HttpResponse(template.render(context = context, request = request))
def equalizeArrays(arr1,arr2):
    while (len(arr1) > len(arr2)):
        arr1.pop(0) #pops from front of array of data with larger size. 
                    #we dont want to compare coins when the later one was non-existent
    while(len(arr2) > len(arr1)):
        arr2.pop(0)
    return arr1, arr2
def axis(array,key_str): #this function searches a passed in array for the key_str and returns the array of only those values
    axis_var = [] #can be x or y usually
    for obj in array:
        axis_var.append(obj[key_str])
    return axis_var
def datetime(x):
    return np.array(x, dtype=np.datetime64)
def parseArr(jsonArr):
    x = []
    y = []
    date = []
    for point in jsonArr:
        x.append(point['x'])
        y.append(point['y'])
        date.append(point['date'])
    return x, y, date 