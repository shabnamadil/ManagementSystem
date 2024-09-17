from django.db import models

class Partner(models.Model):
    name = models.CharField(max_length=255)  # Partner adı
    logo = models.ImageField(upload_to='logos/')  # Logo dosyasının yükleneceği yer
    url = models.URLField(max_length=200, blank=True, null=True)  # Partnerin web sitesi
    
    def __str__(self):
        return self.name