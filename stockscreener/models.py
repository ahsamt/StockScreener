from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import AutoField
import django.utils 

class SavedSearch(models.Model):
    stock = models.CharField(max_length = 5)
    date = models.DateTimeField(default = django.utils.timezone.now)
    notes = models.TextField(max_length=500, blank = True)
    def __str__(self):
        return f"{self.stock} on {self.date}" 
    
class User(AbstractUser): 
    watchlist = models.ManyToManyField(
        SavedSearch, blank=True, related_name="searcher") 
    # add unique constraint 
