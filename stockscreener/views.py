from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.db import models
import pandas as pd
import yfinance as yf

def index(request):
    if request.method == "GET":
        ticker = ["AAPL", "BA", "KO", "IBM", "DIS", "MSFT"]
        stocks = yf.download(ticker, start = "2021-01-01", end = "2021-08-31")
        stocks.to_csv("stocks.csv") 
        stocks = pd.read_csv("stocks.csv", header = [0, 1], index_col = [0], parse_dates = [0])
        return render(request, "stockscreener/index.html")