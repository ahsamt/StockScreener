from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import AutoField
import django.utils 

class User(AbstractUser): 
    pass

class SavedSearch(models.Model):
    stock = models.CharField(max_length = 5)
    date = models.DateTimeField(default = django.utils.timezone.now)
    notes = models.TextField(max_length=500, blank = True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"{self.stock} on {self.date}, watched by {self.user}" 
    

