from types import ClassMethodDescriptorType
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from .models import User, SavedSearch
from django.conf import settings
from django import forms
from django.contrib.auth.decorators import login_required
import os

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import plotly.graph_objects as go

import pandas as pd
import yfinance as yf

from .utils import make_graph_1, make_graph_2, prep_graph_data

class StockForm(forms.Form):
    stock = forms.CharField(label = "Stock name", max_length=5)

class NotesForm(forms.Form):
    notes = forms.CharField(label="Notes", required=True, widget=forms.Textarea)

def index(request):
    user = request.user
    if request.method == "GET":
        stockForm = StockForm()     
        return render (request, "stockscreener/index.html", {"stockForm": stockForm})
    if request.method == "POST":
        if 'stock' in request.POST:
            stockForm = StockForm(request.POST) 
            if stockForm.is_valid():
                stock = stockForm.cleaned_data['stock'].upper()
                
                data1, data2 = prep_graph_data(stock) 
                closing_price = round(data1[stock].iloc[-1],2)
                previous_price = round(data1[stock].iloc[-2],2)
                price_dif = round(previous_price - closing_price, 2)
                perc_dif = round(price_dif/previous_price*100, 2) 
                if price_dif > 0:
                    change = (f"+${price_dif}  (+{perc_dif}%)")
                else:
                    change = (f"-${price_dif}  (-{perc_dif}%)")

                
                graph1 = make_graph_1(data1, stock)
                graph2 = make_graph_2(data2, stock)

                
                if user.is_authenticated:
                    if not len(SavedSearch.objects.filter(user = request.user, stock = stock)):
                        watchlisted = False
                    else:
                        watchlisted = True
            context = {
                "stockForm": stockForm, 
                "stock":stock,
                "closing_price":closing_price,
                "change": change,
                
                "graph1":graph1, 
                "graph2":graph2
                }
                   
        return render(request, "stockscreener/index.html", context)
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
    
@login_required
def watchlist(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            watched_stocks = []
           
            watchlist=SavedSearch.objects.filter(user=request.user)  
            watchlist=sorted(watchlist, key = lambda p: (p.date), reverse=True)
            for item in watchlist:   
                stock = item.stock  
                watchlist_temp = []          
                data1, data2 = prep_graph_data(stock)
                watchlist_temp.append (stock),
                graph1 = make_graph_1(data1, stock)              
                watchlist_temp.append (graph1)
                graph2 = make_graph_2(data2, stock)
                watchlist_temp.append (graph2)
                watched_stocks.append(watchlist_temp)    
        return render(request, "stockscreener/watchlist.html", {'watched_stocks':watched_stocks})
       