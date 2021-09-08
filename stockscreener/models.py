from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils 

class User(AbstractUser):  
    pass

class SavedSearch(models.Model):
    stock = models.CharField(max_length = 5)
    searcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searches")
    date = models.DateTimeField(default = django.utils.timezone.now)