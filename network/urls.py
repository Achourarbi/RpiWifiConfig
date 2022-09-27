from django.urls import path
from . import views

urlpatterns = [
    path('wificonfig/',views.wificonfig, name = "config"),
    ]