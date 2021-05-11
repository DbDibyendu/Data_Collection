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


class InteractiveGraphAPIView(APIView):
    serializer_class = InteractiveSerializer

    def post(self, request, format=None):
        input_stock_ticker = request.data.get('companycode')
        company_code=""
        with open("nasdaq_screener_1615027631665.csv") as f:
            reader = csv.reader(f)
            temp = 0
            for row in reader:
                if(row[0] == input_stock_ticker):
                    company_code = row[0]
                    break
        if company_code == "":
            return Response({"message": "Wrong Company Code"})
        else:
            data_stocks = yf.Ticker(input_stock_ticker)
            data_fetch = data_stocks.history(period='1d', interval='1m')
            raw_data = pd.DataFrame(data=data_fetch)
            raw_data = raw_data.drop(['Dividends', 'Stock Splits'], axis=1)
            #raw_data.to_csv(r'D:\Internship - LSCG\Stocks_Data\All Stocks.csv')
            data = raw_data.drop(['High', 'Low', 'Open', 'Volume'], axis=1)
            data.to_csv(
                r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv', header=False)

            data = pd.read_csv(
                r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv')
            data.columns = ['Datetime', input_stock_ticker]
            data.to_csv(
                r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv', index=None)
            data_plot = pd.read_csv(
                r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv')
            data_plot.plot(x='Datetime', y=[input_stock_ticker], style='-')
            data_plot.head()

            plt.title('Relative price change')
            plt.legend(loc='upper left', fontsize=12)
            plt.xticks(rotation=35)
            plt.tight_layout()
            plt.grid(True)
            fig = px.line(data_plot, x=data_plot['Datetime'], y=[
                        input_stock_ticker], title='Interactive Stocks')
            fig.update_layout(template='plotly_dark')

            plt_div = plot(fig, output_type='div')
            context={'plt_div':plt_div}

            return render(request, 'index.html',  context)


@api_view()
def index2(request):
    # BITCOIN
    scraper = CmcScraper("BTC")
    headers, data = scraper.get_data()
    xrp_json_data = scraper.get_data("json")
    scraper.export("csv", name="btc_all_time")
    df_BTC = scraper.get_dataframe()

    fig = px.line(df_BTC, x=df_BTC['Date'], y=df_BTC['Close'])
    fig.update_layout(template='plotly_dark', autosize=True,
                      width=1500, height=800,)
    graph1 = plot(fig, output_type='div')

    # ETHEREUM
    scraper = CmcScraper("ETH")
    headers, data = scraper.get_data()
    xrp_json_data = scraper.get_data("json")
    scraper.export("csv", name="ETH_all_time")
    df_ETH = scraper.get_dataframe()
    fig = px.line(df_ETH, x=df_ETH['Date'], y=df_ETH['Close'])
    # fig = plt.figure(figsize=(15,12))
    fig.update_layout(template='plotly_dark', autosize=False,
                      width=1500, height=900,)
    graph2 = plot(fig, output_type='div')

    # BINANCE_COIN
    scraper = CmcScraper("BNB")
    headers, data = scraper.get_data()
    xrp_json_data = scraper.get_data("json")
    scraper.export("csv", name="bnb_all_time")
    df_BNB = scraper.get_dataframe()
    fig = px.line(df_BNB, x=df_BNB['Date'], y=df_BNB['Close'])
    # fig = plt.figure(figsize=(15,12))
    fig.update_layout(template='plotly_dark', autosize=False,
                      width=1500, height=900,)
    graph3 = plot(fig, output_type='div')

    # Prediction using Facebook Prophet
    # BTC
    df_BTC_proph = df_BTC[['Date', 'Close']]
    df_BTC_proph = df_BTC.rename(columns={'Date': 'ds', 'Close': 'y'})
    m = Prophet()
    m.fit(df_BTC_proph)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    data = plot_plotly(m, forecast, xlabel='Date', ylabel='Close')
    data.update_layout(autosize=False, width=1500, height=900,)
    graph4 = plot(data, output_type='div')

    data = plot_components_plotly(m, forecast)
    data.update_layout(autosize=False, width=1500, height=900,)
    graph5 = plot(data, output_type='div')

    # ETHEREUM
    df_ETH_proph = df_ETH[['Date', 'Close']]
    df_ETH_proph = df_ETH.rename(columns={'Date': 'ds', 'Close': 'y'})
    m1 = Prophet()
    m1.fit(df_ETH_proph)
    future = m1.make_future_dataframe(periods=365)
    forecast1 = m1.predict(future)
    data = plot_plotly(m1, forecast1, xlabel='Date', ylabel='Close')
    data.update_layout(autosize=False, width=1500, height=900,)
    graph6 = plot(data, output_type='div')

    data = plot_components_plotly(m1, forecast1)
    data.update_layout(autosize=False, width=1500, height=900,)
    graph7 = plot(data, output_type='div')

    # BINANCE
    df_BNB_proph = df_BNB[['Date', 'Close']]
    df_BNB_proph = df_BNB.rename(columns={'Date': 'ds', 'Close': 'y'})
    m2 = Prophet()
    m2.fit(df_BNB_proph)
    future = m2.make_future_dataframe(periods=365)
    forecast2 = m2.predict(future)
    data = plot_plotly(m2, forecast2, xlabel='Date', ylabel='Close')
    data.update_layout(autosize=False, width=1500, height=900,)
    graph8 = plot(data, output_type='div')

    data = plot_components_plotly(m2, forecast2)
    data.update_layout(autosize=False, width=1500, height=900,)
    graph9 = plot(data, output_type='div')

    context = {'graph1': graph1, 'graph2': graph2, 'graph3': graph3, 'graph4': graph4,
               'graph5': graph5, 'graph6': graph6, 'graph7': graph7, 'graph8': graph8, 'graph9': graph9}

    return render(request, 'index2.html', context)
