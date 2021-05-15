import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sweetviz
# from pandas_profiling import ProfileReport
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
import matplotlib.pyplot as plt
import matplotlib  


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
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .models import InteractiveModels,StocksCompanyModels
from .serializers import InteractiveSerializer,StocksCompanySerializer


class CryptoAPI(APIView):
    serializer_class = InteractiveSerializer
    
    def post(self, request, format=None):
        coin = request.data.get('crypto')
        scraper = CmcScraper(coin)
        headers, data = scraper.get_data()
        xrp_json_data = scraper.get_data("json")
        # scraper.export("csv", name="btc_all_time")
        df_BTC = scraper.get_dataframe()
        fig = px.line(df_BTC, x=df_BTC['Date'], y=df_BTC['Close'])
        fig.update_layout(template='plotly_dark', autosize=True,
                        width=1500, height=800,)

        graph1 = plot(fig, output_type='div')
        context = {'graph1': graph1}
        # return render(request,"index2.html",context)
        return Response(context)


class StocksCompanyAPI(APIView):
    serializer_class =  StocksCompanySerializer 


    def post(self , request , format = None):
        input_stock_ticker = request.data.get('companycode')

    
        data_stocks = yf.Ticker(input_stock_ticker)
        data_fetch = data_stocks.history(period='1d', interval='1m')
        raw_data = pd.DataFrame(data=data_fetch)
        raw_data = raw_data.drop(['Dividends','Stock Splits'], axis=1)
        #raw_data.to_csv(r'D:\Internship - LSCG\Stocks_Data\All Stocks.csv')
        data = raw_data.drop(['High','Low','Open','Volume'], axis=1)
        data.to_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv',header=False)

        data = pd.read_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv')
        data.columns = ['Datetime',input_stock_ticker]
        data.to_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv',index=None)
        data_plot = pd.read_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv')
        data_plot.plot(x='Datetime',y=[input_stock_ticker],style='-')
        data_plot.head()

        plt.title('Relative price change')
        plt.legend(loc='upper left', fontsize=12)
        plt.xticks(rotation=35)
        plt.tight_layout()
        plt.grid(True)
        fig = px.line(data_plot,x=data_plot['Datetime'],y=[input_stock_ticker],title='Interactive Stocks')
        fig.update_layout(template='plotly_dark')
        
        graph1 = plot(fig, output_type='div')
        context = {'graph1': graph1}
        # return render(request,"index2.html",context)
        return Response(context)
