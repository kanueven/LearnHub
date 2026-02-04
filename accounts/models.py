from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#Custome user model extending an abstract user  for profile, followers,avatars etc.
class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username