from django.db import models
from .bot import Bot

class Chat(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=255)


    username = models.CharField(max_length=255, blank=True, null=True)  
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    chat_type = models.CharField(max_length=20, blank=True, null=True)  
    title = models.CharField(max_length=255, blank=True, null=True)   

    is_active = models.BooleanField(default=True)   
    joined_at = models.DateTimeField(auto_now_add=True)  
    last_interaction = models.DateTimeField(blank=True, null=True)  

    class Meta:
        unique_together = ('bot', 'chat_id')