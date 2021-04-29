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

import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as py

from rest_framework.response import Response
from rest_framework.decorators import api_view

from cryptocmd import CmcScraper


@api_view()
def index(request):
    data_stocks = yf.Tickers('MSFT AAPL GOOG TSLA FB AMZN')
    #print(data_stocks.tickers.AMZN.info)
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    data_fetch = data_stocks.history(period='1d', interval='1m')
    #print(data_fetch)
    raw_data = pd.DataFrame(data=data_fetch)
    raw_data = raw_data.drop(['Dividends', 'Stock Splits'], axis=1)
    raw_data.to_csv(r'D:\Internship - LSCG\Stocks_Data\All Stocks.csv')
    data = raw_data.drop(['High', 'Low', 'Open', 'Volume'], axis=1)
    data.to_csv(r'D:\Internship - LSCG\Stocks_Data\Closing Stocks.csv', header=False)

    data = pd.read_csv(r'D:\Internship - LSCG\Stocks_Data\Closing Stocks.csv')
    data.columns = ['Datetime', 'AAPL', 'AMZN', 'FB', 'GOOG', 'MSFT', 'TSLA']
    # print(data.head())
    data.to_csv(r'D:\Internship - LSCG\Stocks_Data\Closing Stocks.csv', index=None)
    data_plot = pd.read_csv(r'D:\Internship - LSCG\Stocks_Data\Closing Stocks.csv')

    amzn=data_plot['AMZN'].values.tolist() 
    date=data_plot['Datetime'].values.tolist() 
    tsla=data_plot['TSLA'].values.tolist() 
    fb=data_plot['FB'].values.tolist()
    msft=data_plot['MSFT'].values.tolist()
    aapl=data_plot['AAPL'].values.tolist()
    goog=data_plot['GOOG'].values.tolist()
    
    fig = px.line(data_plot,x=data_plot['Datetime'],y=['AMZN','AAPL','MSFT','TSLA','FB','GOOG'],title='Interactive Stocks')
    fig.update_layout(template='plotly_dark')
    plt_div = plot(fig, output_type='div')

    context={"amzn":amzn, 'date':date, 'tsla':tsla, 'fb':fb, 'msft': msft, 'aapl': aapl,'goog':goog, 'plt_div':plt_div}

    return render(request, 'index.html', context)


@api_view()
def index2(request):
    #BITCOIN
    scraper = CmcScraper("BTC")
    headers, data = scraper.get_data()
    xrp_json_data = scraper.get_data("json")
    scraper.export("csv", name="btc_all_time")
    df_BTC = scraper.get_dataframe()

    fig = px.line(df_BTC,x=df_BTC['Date'],y=df_BTC['Close'])
    fig.update_layout(template='plotly_dark',autosize=True,width=1500,height=800,)
    graph1 = plot(fig, output_type='div')

    #ETHEREUM
    scraper = CmcScraper("ETH")
    headers, data = scraper.get_data()
    xrp_json_data = scraper.get_data("json")
    scraper.export("csv", name="ETH_all_time")
    df_ETH = scraper.get_dataframe()
    fig = px.line(df_ETH,x=df_ETH['Date'],y=df_ETH['Close'])
    #fig = plt.figure(figsize=(15,12))
    fig.update_layout(template='plotly_dark',autosize=False,width=1500,height=900,)
    graph2 = plot(fig, output_type='div')

    #BINANCE_COIN
    scraper = CmcScraper("BNB")
    headers, data = scraper.get_data()
    xrp_json_data = scraper.get_data("json")
    scraper.export("csv", name="bnb_all_time")
    df_BNB = scraper.get_dataframe()
    fig = px.line(df_BNB,x=df_BNB['Date'],y=df_BNB['Close'])
    #fig = plt.figure(figsize=(15,12))
    fig.update_layout(template='plotly_dark',autosize=False,width=1500,height=900,)
    graph3 = plot(fig, output_type='div')
    
    context={'graph1':graph1, 'graph2':graph2,'graph3':graph3}
    return render(request, 'index2.html', context)