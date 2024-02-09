"""
URL configuration for vechileCount project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path("",views.landing, name='landing'),
    path("daftar",views.daftar, name='daftar'),
    path("base", lambda request: redirect('home'), name='base'),
    path("home",views.home, name='home'),
    path("history",views.history, name='history'),
    path('test',views.count),
]
