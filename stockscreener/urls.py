from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name = "index"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("ticker_list", views.ticker_list, name = "ticker_list"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register, name = "register"),

     # API Routes
     path("saved_searches", views.saved_searches, name = "saved_searches"),
     path("saved_searches/<int:search_id>", views.saved_search, name="saved_search")
]