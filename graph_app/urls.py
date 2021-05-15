from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CryptoAPI,StocksCompanyAPI

urlpatterns = [
    path('crypto-graph/', CryptoAPI.as_view()),
    path('stocks-graph/', StocksCompanyAPI.as_view()),
]
