from django.contrib import admin
from .models import User, SavedSearch

admin.site.register(User)

admin.site.register(SavedSearch)