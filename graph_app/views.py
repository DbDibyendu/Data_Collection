from django.shortcuts import render
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sweetviz
# from pandas_profiling import ProfileReport
import plotly
import plotly.graph_objects as go
import plotly.express as px

import base64
import urllib
import io
from io import BytesIO
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

from rest_framework.response import Response
from rest_framework.decorators import api_view

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

    d1=data_plot['AMZN'].values.tolist() 
    t=data_plot['Datetime'].values.tolist() 
    d2=data_plot['TSLA'].values.tolist() 
    d3=data_plot['FB'].values.tolist()
    d4=data_plot['MSFT'].values.tolist()
    d5=data_plot['AAPL'].values.tolist()
    d6=data_plot['GOOG'].values.tolist()
    context={'d1': d1,'t':t,'d2':d2, 'd3':d3, 'd4':d4, 'd5':d5,'d6':d6}

    return render(request, 'index.html', context)
