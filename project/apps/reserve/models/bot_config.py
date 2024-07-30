from django.db import models

class BotConfig(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name