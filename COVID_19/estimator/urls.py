from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('xml/', views.xml, name="xml"),
    path('json/', views.json, name="json"),
    path('logs/', views.logs, name="logs"),
]