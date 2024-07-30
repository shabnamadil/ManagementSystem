from django.db import models

class BaseModel(models.Model):
    """All models extends this model"""
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True