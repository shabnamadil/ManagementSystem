from django.db import models

from utils.models.base_model import BaseModel


class IP(BaseModel):
    view_ip = models.GenericIPAddressField(
        'IP ünvanı', 
        editable=False
    )

    class Meta:
        verbose_name = ('IP ünvanı')
        verbose_name_plural = ('IP ünvanları')

    def __str__(self) -> str:
        return self.view_ip