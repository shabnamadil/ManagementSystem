from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """All models extends this model"""
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

    @property
    def created_date(self):
        local_created = timezone.localtime(self.created)
        return local_created.strftime('%d/%m/%Y, %H:%M')