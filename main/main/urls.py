"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import redirect
from . import myRedirects
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('apps.bokehGraphs.urls')), #rendered pages
    url(r'^components/', include('apps.components.urls')), #html components, calls 2nd level
    url(r'^api/', include('apps.api.urls')), #1st level api
    url(r'^ajax/', include('apps.ajax.urls')), #2nd level api ajax calls to first level
    #url(r'^$', myRedirects.home),
]
