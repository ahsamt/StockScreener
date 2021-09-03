from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from .models import User

import pandas as pd
import yfinance as yf

def index(request):
    if request.method == "GET":
        ticker = ["AAPL", "BA", "KO", "IBM", "DIS", "MSFT"]
        stocks = yf.download(ticker, start = "2021-01-01", end = "2021-08-31")
        stocks.to_csv("stocks.csv") 
        stocks = pd.read_csv("stocks.csv", header = [0, 1], index_col = [0], parse_dates = [0])
        return render(request, "stockscreener/index.html")

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