from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Save the instance, ensuring only one instance exists."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Load or create the singleton instance."""
        try:
            return cls.objects.get(pk=1)
        except ObjectDoesNotExist:
            instance = cls(pk=1)
            instance.save()
            return instance
