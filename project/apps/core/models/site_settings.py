from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, verbose_name="Site Name")
    logo = models.ImageField(upload_to='logos/', verbose_name="Site Logo")
    favicon = models.ImageField(upload_to='favicons/', verbose_name="Favicon")
    footer_text = models.TextField(verbose_name="Footer Text", blank=True, null=True)
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name
