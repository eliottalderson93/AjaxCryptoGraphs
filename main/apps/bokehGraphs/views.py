from django.shortcuts import render, HttpResponse, redirect, render_to_response
import requests, json
def graph(request):
    context = {
        "plots" : [],
    }
    print("you are in the home render")
    return render(request,"bokehGraphs/graphs.html", context)