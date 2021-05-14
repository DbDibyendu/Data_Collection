from django.contrib import admin
from django.urls import path , include 
from  . import views 
from .views import CryptoAPI, Forecast

urlpatterns = [
    path('graph/' , CryptoAPI.as_view()),
    path('graph2/' , Forecast.as_view()),
]
