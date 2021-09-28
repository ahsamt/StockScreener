from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import AutoField
import django.utils 

class User(AbstractUser): 
    pass

class SavedSearch(models.Model):
    stock = models.CharField(max_length = 5)
    stock_full = models.CharField(max_length = 20)
    date = models.DateTimeField(default = django.utils.timezone.now)
    notes = models.TextField(max_length=500, blank = True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watchlist")
   
    class Meta:
       constraints = [
           models.UniqueConstraint(fields=['stock', 'user'], name = "unique_searches")
       ]

    def serialize(self):
        return {
            "id":self.id,
            "stock":self.stock,
            "user":self.user.username,
            "date": self.date,
            "notes":self.notes
        }
   
    def __str__(self):
        return f"{self.stock} on {self.date}, watched by {self.user}" 
    

