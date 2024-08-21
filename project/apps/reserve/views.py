from django.http import HttpResponse
from .utils.checkers.post_checker import ScheduledPostChecker

def reserve(request):
    checker = ScheduledPostChecker()
    checker.check_posts()
    return HttpResponse("test")