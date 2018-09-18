from django.shortcuts import render
import json,requests
from django.http import HttpResponse
from time import gmtime, strftime, mktime
from datetime import date, datetime, time
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
#this function is the second level api route that calls the other routes in the api and serves a dict of x and y values for the ajax bokeh plot on our graphing/rendering server
#this function calls once and is used when we want to get a bokeh Ajax source for one coin only e.g. price vs time of litecoin
@csrf_exempt
def ajaxSource(request, x_key,y_key,coinParam = False, beginParam = False, endParam = False):
    print("you are in the ajaxSource view")
    output = {
        "x" : [None],
        "y" : [None]
    }   
    #building the URL to one of the three above routes
    apiURL = "http://18.220.161.116/api/"
    if(coinParam): #calls a price vs time
        #x = time y = price
        #print("there is coinParam")
        apiURL += str(coinParam)
        if(beginParam):
            apiURL += "/" + str(beginParam)
        if(endParam):
            apiURL += "/" + str(endParam)
        print("api URL call from ajaxSource:",apiURL)
        rawData = requests.get(apiURL).json()
    else: #calls default
        #print("there is NOT coinParam")
        print("api URL call from ajaxSource:",apiURL)
        rawData = requests.get(apiURL).json()
    if (rawData['response'] != 200): #tells failed api call
        print("bad response, not 200")
        pass #lets output be None
    else:
        #processes raw Data into x and y axes
        output = { #x is price, y is time usually
            "x" : axis(rawData['PricePoint'], str(x_key)),
            "y" : axis(rawData['PricePoint'], str(y_key))       
        }
    return HttpResponse(json.dumps(output, sort_keys=True, indent=1, cls=DjangoJSONEncoder),content_type="application/json")
#this function is one of the second level api route that calls the other routes in the api and serves a dict of x and y values for the ajax bokeh plot on our graphing/rendering server
#this function calls twice and is used when both axes need a different call e.g. for comparing two coin data
@csrf_exempt
def doubleAjaxSource(request, x_key,y_key,coinParamOne, coinParamTwo, beginParam = False, endParam = False):
    print("you are in the doubleAjaxSource view")
    output = {
        "x" : [None],
        "y" : [None]
    } 
    coinOneURL = "http://18.220.161.116/api/"
    coinTwoURL = "http://18.220.161.116/api/"
    #build the two calls
    coinOneURL += str(coinParamOne)
    coinTwoURL += str(coinParamTwo)
    if(beginParam):
        coinOneURL += "/" + str(beginParam)
        coinTwoURL += "/" + str(beginParam)
    if(endParam):
        coinOneURL += "/" + str(endParam)
        coinTwoURL += "/" + str(endParam)
    #call the API
    xRawData = requests.get(coinOneURL).json()
    yRawData = requests.get(coinTwoURL).json() 
    #failed api call 
    if((xRawData['response'] != 200) or (yRawData['response'] != 200)):
        pass #lets output be None
    else:
        #processes raw Data into x and y axes
        print("x full json: ",list(xRawData.keys()))
        print("y full json: ",list(yRawData.keys()))
        pricePointArr = joinOnDate(xRawData['PricePoint'],yRawData['PricePoint'],str(x_key),str(y_key))
    return HttpResponse(json.dumps(pricePointArr, sort_keys=True, indent=1, cls=DjangoJSONEncoder),content_type="application/json")
def axis(array,key_str): #this function searches a passed in array for the key_str and returns the array of only those values
    print("axis function\nProcessing Array:\n",array[0])
    print("filtering by: ",key_str)
    axis_var = [] #can be x or y usually
    for obj in array:
        axis_var.append(obj[key_str])
    return axis_var
def joinOnDate(pricePointArrX,pricePointArrY,nameX,nameY,measureKey = "Price",commonKey = "Time", date = True): #pass in pricePoint arrays
    #this function returns an enhanced pricePoint array, where the dates match
    print("joinOnDate function")
    joinedArr = []
    for obj1 in pricePointArrX:
        date1 = datetime.strptime(obj1[commonKey],"%Y-%m-%d")
        for obj2 in pricePointArrY:
            date2 = datetime.strptime(obj2[commonKey],"%Y-%m-%d")
            if(date):
                if(date1 == date2):
                    #join these dates
                    #print("join these:",obj1,obj2)
                    joinObj = {
                        "x" : obj1[measureKey],
                        "y" : obj2[measureKey],
                        "date" : date1.strftime("%Y-%m-%d"),
                        "xName" : nameX + " " + measureKey,
                        "yName" : nameY + " " + measureKey
                        }
                    joinedArr.append(joinObj)
                else:
                    pass #do not join
            else: #not a date
                if(obj1[commonKey] == obj2[commonKey]):
                    joinObj = {
                        "x" : obj1[measureKey],
                        "y" : obj2[measureKey],
                        "date" : date1.strftime("%Y-%m-%d"),
                        "xName" : nameX,
                        "yName" : nameY
                        }
                    joinArr.append(joinObj)
                else:
                    pass #do not join
    print("joined object example:",joinedArr[0])
    return joinedArr
