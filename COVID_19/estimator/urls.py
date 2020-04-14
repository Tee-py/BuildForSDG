from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('api/v1/on-covid-19/', views.endpoint, name="endpoint"),
    path('api/v1/on-covid-19/xml', views.xml, name="xml"),
    path('api/v1/on-covid-19/json', views.json, name="json"),
    path('api/v1/on-covid-19/logs/', views.logs, name="logs"),
]