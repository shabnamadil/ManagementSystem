from django.utils import timezone
from utils.slugify.custom_slugify import custom_slugify


def upload_to(instance, filename):
    sanitized_full_name = custom_slugify(instance.full_name)
    date_str = instance.created.strftime('%Y-%m-%d') if instance.created else timezone.now().strftime('%Y-%m-%d')
    extension = filename.split('.')[-1]
    new_filename = f'{sanitized_full_name}_{date_str}.{extension}'
    return f'workspace-client-images/{sanitized_full_name}/{new_filename}'