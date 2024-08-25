from django.utils import timezone
from ...models import PlatformSpecificSchedule
from .instagram_publish_checker import InstagramPublishChecker

from apps.notification.utils.services.notification import NotificationService

import logging


class ScheduledPostChecker:
    def __init__(self):
        self.checkers = {
            'instagram': InstagramPublishChecker(),
            # Add checkers for other platforms as needed
        }

    def check_posts(self):
        """
        Checks for scheduled posts that are due for publishing and triggers their publishing process.
        """
        # Get all schedules where the scheduled time is in the past and the status is still 'scheduled'
        unpublished_schedules = PlatformSpecificSchedule.objects.filter(
            scheduled_date__lte=timezone.now(),
            status='scheduled'
        )


        for schedule in unpublished_schedules:
            checker = self.checkers.get(schedule.platform.name)
            if checker:
                try:
                    checker.check_post(schedule)  # Trigger the platform-specific publishing check

                    # If the post status changed to 'published' or 'failed', send notifications
                    if schedule.status in ['published', 'failed']:
                        print(schedule.status)
                except Exception as e:
                    # Handle any potential errors during the publishing check
                    logging.error(f"Error checking scheduled post {schedule.id}: {e}")
                    # You might want to update the schedule status to 'failed' here and possibly send an error notification