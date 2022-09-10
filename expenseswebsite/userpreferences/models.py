
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserPreference(models.Model):
    currency = models.TextField(max_length=255,blank=True, null=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)


    def __str__(self):
        
        return str(self.user) + ' s' +'settings'