from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from .models import User
from django.conf import settings
from django import forms
import os

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import plotly.graph_objects as go

import pandas as pd
import yfinance as yf

class StockForm(forms.Form):
    stock = forms.CharField(label = "Stock name", max_length=5)


def index(request):
    
    if request.method == "GET":
        stockForm = StockForm()
             
        return render(request, "stockscreener/index.html", {"stockForm": stockForm})
   
    if request.method == "POST":
        if 'stock' in request.POST:
            stockForm = StockForm(request.POST) 
            if stockForm.is_valid():
                stock = stockForm.cleaned_data['stock']
                ticker = [stock]
                num_months = 6
                end_date = date.today()
                start_date = end_date + relativedelta(months = -num_months) 
                
                stocks = yf.download(ticker, start = start_date, end = end_date)
                stocks.to_csv("stocks.csv")
                stocks = pd.read_csv("stocks.csv", header = [0], index_col = [0], parse_dates = [0])
                stocks = stocks.reset_index()
                dates = stocks.loc[:, "Date"].copy()
                close = stocks.loc[:, "Close"].copy()

                
                fig = go.Figure()
                fig.add_trace(go.Scatter(name="Graph", x=dates, y=close ))

                graph = fig.to_html(full_html=False, default_height=500, default_width=700)

                
        return render(request, "stockscreener/index.html", {"stockForm": stockForm, "graph":graph})

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "stockscreener/login.html", {"message":"Invalid username and/or password"})
    else:
        return render(request, "stockscreener/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Make sure password matches password confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "stockscreener/register.html", {
                "message":"Please make sure the passwords match"
            })

        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "stockscreener/register.html",{
                "message":"Sorry, this username is not available"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "stockscreener/register.html")