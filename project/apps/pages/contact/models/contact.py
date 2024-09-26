from django.db import models

from utils.models.base_model import BaseModel


class Contact(BaseModel):
    name = models.CharField(
        'Ad',
        max_length=100
    )
    surname = models.CharField(
        'Soyad',
        max_length=100
    )
    email = models.EmailField(
        'Email'
    )
    mobile_number = models.CharField(
        'Telefon nömrəsi',
        max_length=20,
        null=True, blank=True,
        help_text='Yalnız rəqəm daxil edin'
    )
    message = models.TextField(
        'Mesaj'
    )

    class Meta:
        verbose_name = 'Mesaj'
        verbose_name_plural = 'Mesajlar'
        indexes = [models.Index(fields=['created'])]
        ordering = ('-created',)

    def __str__(self) -> str:
        return f'{self.name} {self.surname}-dən mesaj'