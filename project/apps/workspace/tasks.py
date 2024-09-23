from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from ..workspace.models import Subtask

@shared_task(name='workspace.tasks.notify_assignee')
def notify_assignee(subtask_id):
    try:
        subtask = Subtask.objects.get(pk=subtask_id)
    except Subtask.DoesNotExist:
        return

    if subtask.assigned_to:
        context = {
            'subtask': subtask,
            'start_date': subtask.started_date,
            'deadline': subtask.deadline
        }
        message = render_to_string('components/mail/notify_assignee.html', context)
        send_mail(
            'Your subtask is about to start',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subtask.assigned_to.user.email],
            fail_silently=False,
            html_message=message
        )