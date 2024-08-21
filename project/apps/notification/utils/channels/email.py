from django.core.mail import send_mail
from django.conf import settings

from .base import NotificationChannel

class EmailChannel(NotificationChannel):
    """
    Sends notifications via email.
    """

    def send_notification(self, user, content, to_email):
        """
        Sends an email notification.
        """
        try:
            subject = "Notification from [Your App Name]"  # Set a suitable subject
            from_email = settings.DEFAULT_FROM_EMAIL  # Use the default from email in your settings
            recipient_list = [to_email]  # List of recipient email addresses

            send_mail(subject, content, from_email, recipient_list)
        except Exception as e:
            # Error handling - log or perform other actions as needed
            print(f"Email sending error: {e}")