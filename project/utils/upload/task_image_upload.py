from django.utils import timezone
from utils.slugify.custom_slugify import custom_slugify


def upload_to(instance, filename):
    sanitized_title = custom_slugify(instance.title)
    client = instance.project.workspace_project.client.full_name
    date_str = instance.created.strftime('%Y-%m-%d') if instance.created else timezone.now().strftime('%Y-%m-%d')
    extension = filename.split('.')[-1]
    new_filename = f'{sanitized_title}_{date_str}.{extension}'
    return f'task-images/{client}/{new_filename}'