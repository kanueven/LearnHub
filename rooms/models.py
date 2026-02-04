from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey('topics.Topic', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200) #Room title
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated_at = models.DateTimeField(auto_now=True) # Updates on every save  
    created = models.DateTimeField(auto_now_add=True)  # Set once on creation 
    
    class Meta:
        ordering = ['-updated_at', '-created']
        
    def __str__(self):
        return self.name
# each room will have a message
class Message(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # Updates on every save  
    created = models.DateTimeField(auto_now_add=True)  # Set once on creation
    
    
    
    def __str__(self):
        return self.body[0:50]


