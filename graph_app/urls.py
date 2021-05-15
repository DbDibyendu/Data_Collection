from django.contrib import admin
from django.urls import path , include 
from  . import views 
from .views import CryptoAPI

urlpatterns = [
    path('graph/' , CryptoAPI.as_view()),
]
