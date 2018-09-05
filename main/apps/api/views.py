from django.shortcuts import render
import json,requests
from django.http import HttpResponse
from time import gmtime, strftime, mktime
from datetime import date, datetime, time
from django.core.serializers.json import DjangoJSONEncoder
#this view serves up json data from my heroku proxy server
#the request is abstracted in the proxycall function and each of the three routes calls it with a different kind of URL
#these are the first level api calls that communicates with our proxy server based on how we want to use the base API
def bitcoin(request): #default route
    print("default API route")
    URL = "https://fierce-fortress-88237.herokuapp.com/" #proxy server
    URL += "bitcoin" #seperate line
    json_output = proxyCall(URL)
    json_output['name'] = "bitcoin"
    json_output['from'] = ["all","all"]
    return HttpResponse(json.dumps(json_output, sort_keys=True, indent=1, cls=DjangoJSONEncoder), content_type="application/json")
def allCoin(request,coin):
    print("one coin API route")
    URL = "https://fierce-fortress-88237.herokuapp.com/" #proxy server
    URL += str(coin)
    json_output = proxyCall(URL)
    json_output['name'] = str(coin)
    json_output['from'] = ["all","all"]
    return HttpResponse(json.dumps(json_output, sort_keys=True, indent=1, cls=DjangoJSONEncoder), content_type="application/json")
def timeCoin(request, coin, begin, end):
    print("one coin API route with RANGE")
    URL = "https://fierce-fortress-88237.herokuapp.com/" #proxy server
    URL += str(coin)
    URL += "/"
    URL += str(begin)
    URL += "/"
    URL += str(end)
    #print(URL)
    json_output = proxyCall(URL)
    json_output['name'] = str(coin)
    json_output['from'] = [begin,end]
    return HttpResponse(json.dumps(json_output, sort_keys=True, indent=1, cls=DjangoJSONEncoder),content_type="application/json")
#this function calls our proxy server which is used for the first level api routes above
def proxyCall(URL):
    response = requests.get(URL)
    apiCall = {}
    apiCall['response'] = response.status_code
    apiCall['PricePoint'] = {}
    if response.status_code != 200: #checks if get was successful and breaks if not
        print('BAD CODE::',response.status_code)
        return apiCall
    # Translate to JSON
    data = response.json()
    #print('JSON::', data['price_usd'])
    # Storing date and price into Object List
    max_len = int(len(data['price_usd']))
    datePrice = []
    for i in range(0,max_len): # organize data 
                               # the zero represents the beginning of a returned array
                               # remember the begin and end time is based on the URL not this for loop
        time = datetime.fromtimestamp(int((data['price_usd'][i][0])/1000)).strftime('%Y-%m-%d')
        price = data['price_usd'][i][1]
        datePrice.append({'Time': time,'Price': price}) #this needs to be abstracted for different x and y variables
        # return the objectList
    #print('ARRAY LENGTH::',len(datePrice))
    apiCall['PricePoint'] = datePrice
    return apiCall