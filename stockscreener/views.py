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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import plotly.graph_objects as go

import pandas as pd
import yfinance as yf

from .utils import get_change_info, make_graph_1, make_graph_2, prep_graph_data

class StockForm(forms.Form):
    stock = forms.CharField(label = "Stock name", max_length=5)

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
                closing_price, change = get_change_info(data1, stock)
                graph1 = make_graph_1(data1, stock, 470, 630)
                graph2 = make_graph_2(data2, stock, 470, 630)

                watchlisted = False
                stockID = None

                if user.is_authenticated:
                    searchObj = SavedSearch.objects.filter(user = request.user, stock = stock)
                    if len(searchObj):                      
                        watchlisted = True
                        stockID =  searchObj[0].id

            context = {
                "stockForm": stockForm, 
                "stock":stock,
                "stockID":stockID,
                "closing_price":closing_price,
                "change": change,
                "watchlisted":watchlisted, 
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
                
                watchlist_temp = {} 
                watchlist_temp["stock"] = stock
                watchlist_temp["data1"], watchlist_temp["data2"] = prep_graph_data(stock)     
                watchlist_temp["closing_price"], watchlist_temp["change"] = get_change_info(watchlist_temp["data1"], stock)
        
                watchlist_temp["graph1"] = make_graph_1(watchlist_temp["data1"], stock, 500, 750)              
                
                watchlist_temp["graph2"] = make_graph_2(watchlist_temp["data2"], stock, 500, 750)
                
                watchlist_temp["notes"] = item.notes 
              
                watchlist_temp["stockID"]= item.id 

                watched_stocks.append(watchlist_temp)    
                
                
        return render(request, "stockscreener/watchlist.html", {'watched_stocks':watched_stocks})

@csrf_exempt
@login_required
def saved_searches(request):

    # Creating a new saved search must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check received data emails
    data = json.loads(request.body)
    
    stock = data.get("stock")
    if stock == [""]:
        return JsonResponse({
            "error": "Stock name is required."
        }, status=400)
    
    
    # Create a saved search for the logged in user
    
    savedSearch = SavedSearch(
            user = request.user,
            stock = stock,
            
        )
    savedSearch.save()
    search_id = savedSearch.id
       

    return JsonResponse({"message": "Search saved successfully", "id":search_id}, status=201)

@csrf_exempt
@login_required
def saved_search(request, search_id):
   
    # Query for requested search
    try:
        search = SavedSearch.objects.get(user=request.user, pk=search_id)
    except SavedSearch.DoesNotExist:
        return JsonResponse({"error": "No such search has been saved for this user."}, status=404)

    # Return saved search contents
    if request.method == "GET":
        return JsonResponse(search.serialize())

    # Update notes for the saved search
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("notes") is not None:
            search.notes = data["notes"]
        search.save()
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        search.delete()
        return HttpResponse(status=204)

    # Search must be via GET, PUT or DELETE
    else:
        return JsonResponse({
            "error": "GET, PUT or DELETE request required."
         }, status=400)

