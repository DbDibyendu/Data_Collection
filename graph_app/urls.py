from django.contrib import admin
from django.urls import path , include 
from  . import views 
from .views import InteractiveGraphAPIView

urlpatterns = [
    path('graph/' , InteractiveGraphAPIView.as_view()),
    path('graph2/' , views.index2 , name = 'index2'),

]
