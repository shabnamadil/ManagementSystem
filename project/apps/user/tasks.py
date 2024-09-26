from django.contrib.auth import get_user_model

from celery import shared_task

from utils.otp.send_otp import send_otp_email
from utils.otp.generate_otp import generate_otp

User = get_user_model()


@shared_task(name="apps.user.tasks.send_registration_otp")
def send_registration_otp(email):
    try:
        user = User.objects.get(email=email)
        otp = generate_otp(user)
        send_otp_email(email, otp)
    except User.DoesNotExist:
        raise Exception(f"No user found with email: {email}")