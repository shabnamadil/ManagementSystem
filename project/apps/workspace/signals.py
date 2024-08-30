
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.db import transaction
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.sites.models import Site
from django.utils import timezone

from datetime import timedelta
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

from apps.workspace.models import (
    Workspace,
    Task,
    Subtask,
    SubtaskStatus
)

User = get_user_model()


@receiver(post_save, sender=Subtask)
def notify_admin_to_check_task(sender, instance, **kwargs):
        if instance.completed:
            task_admins = instance.task.assigned_members.filter(role='Admin')
            assigned_to_email = instance.assigned_to.user.email
            current_site = Site.objects.get_current()

            url = f"http://{current_site.domain}{reverse_lazy('task-detail', args={instance.task.pk})}"

            context = {
                  'subtask' : instance,
                  'subtask_assigned_to' : assigned_to_email,
                  'url': url
            }
            subject = f"Admin üçün yoxlamaq vaxtıdır."
            message = render_to_string('components/mail/check_subtask.html', context)

            for admin in task_admins:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin.user.email],
                    fail_silently=False,
                    html_message=message,
                )

@receiver(post_save, sender=Subtask)
def create_subtask_status(sender, created, instance, **kwargs):
      if created:
            SubtaskStatus.objects.get_or_create(subtask=instance)
            task = instance.task
            task.completed = False
            task.save()


@receiver(post_save, sender=Subtask)
def notify_next_assignee(sender, instance, **kwargs):
    if instance.completed:
        # Find the next subtask in the order
        next_subtask = Subtask.objects.filter(task=instance.task, started_date__gt=instance.started_date).order_by('started_date').first()

        context = {
            'current_subtask' : instance,
            'next_subtask' : next_subtask,
        }

        message = render_to_string('components/mail/notify_next_assignee.html', context)
        
        if next_subtask:
            send_mail(
                'Your subtask is ready to start',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [next_subtask.assigned_to.user.email],
                fail_silently=False,
                html_message=message,
            )


@receiver(post_save, sender=Subtask)
def notify_subtask_assignee_before_started(sender, instance, created, **kwargs):
    if created:
        current_time = timezone.now()
        subtask_started_date = instance.started_date
        difference = subtask_started_date - current_time

        if difference > timedelta(minutes=30):
            # Calculate the time to schedule the task
            schedule_time = subtask_started_date - timedelta(minutes=30)
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=schedule_time.minute,
                hour=schedule_time.hour,
                day_of_month=schedule_time.day,
                month_of_year=schedule_time.month,
                day_of_week='*'
            )

            PeriodicTask.objects.update_or_create(
                name=f'notify_assignee_{instance.id}',
                defaults={
                    'task': 'workspace.tasks.notify_assignee',
                    'crontab': schedule,
                    'one_off': True,
                    'args': json.dumps([instance.id]),
                    'enabled': True
                }
            )
