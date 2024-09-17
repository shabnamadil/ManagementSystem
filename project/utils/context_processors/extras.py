import datetime

from apps.core.models import SiteSettings

def extras(request):
    context={
        'current_year': datetime.datetime.now().year,
        'current_time': datetime.datetime.now(),
        'settings': SiteSettings.objects.first()
    }
    return context