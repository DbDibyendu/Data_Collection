from django.shortcuts import render
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sweetviz
# from pandas_profiling import ProfileReport
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot

import base64
import urllib
import io
from io import BytesIO
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from django.shortcuts import render, redirect
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as py

from rest_framework.response import Response
from rest_framework.decorators import api_view

from cryptocmd import CmcScraper
from prophet.plot import plot_plotly, plot_components_plotly
from fbprophet import Prophet
import csv
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .models import InteractiveModels
from .serializers import InteractiveSerializer


class CryptoAPI(APIView):
    serializer_class = InteractiveSerializer
    
    def post(self, request, format=None):
        coin = request.data.get('crypto')
        scraper = CmcScraper(coin)
        headers, data = scraper.get_data()
        xrp_json_data = scraper.get_data("json")
        scraper.export("csv", name="btc_all_time")
        df_BTC = scraper.get_dataframe()
        fig = px.line(df_BTC, x=df_BTC['Date'], y=df_BTC['Close'])
        fig.update_layout(template='plotly_dark', autosize=True,
                        width=1500, height=800,)
        graph1 = plot(fig, output_type='div')

        context = {'graph1': graph1}

        return Response(context)

class Forecast(APIView):
    serializer_class = InteractiveSerializer
    
    def post(self, request, format=None):
        coin = request.data.get('crypto')
        scraper = CmcScraper(coin)
        headers, data = scraper.get_data()
        xrp_json_data = scraper.get_data("json")
        scraper.export("csv", name="btc_all_time")
        df_BTC = scraper.get_dataframe()
        df_BTC_proph = df_BTC[['Date', 'Close']] 
        df_BTC_proph = df_BTC.rename(columns={'Date':'ds', 'Close':'y'}) 
        m=Prophet()
        m.fit(df_BTC_proph)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)
        fig1 = plot_plotly(m, forecast,xlabel='Date', ylabel='Close')
        fig1.update_layout(autosize=True,width=1500, height=800)
        graph1 = plot(fig1, output_type='div')

        fig2 = plot_components_plotly(m, forecast)
        fig2.update_layout(autosize=True,width=1500, height=800)
        graph2 = plot(fig2, output_type='div')

        context={'graph1':graph1, 'graph2':graph2}
        return Response(context)
        # return render(request,'index2.html',context)