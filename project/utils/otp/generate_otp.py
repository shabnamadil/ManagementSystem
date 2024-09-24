import random
from django.core.exceptions import ObjectDoesNotExist

from apps.user.models.otp import OTP

def generate_otp(user, length=6):
    otp_chars = "0123456789"
    otp = ''.join(random.choice(otp_chars) for _ in range(length))

    try:
        existing_otp = OTP.objects.get(user=user)
        existing_otp.otp = otp
        existing_otp.save()
        return existing_otp 

    except ObjectDoesNotExist:
        otp_instance = OTP.objects.create(user=user, otp=otp)
        return otp_instance

    except Exception as e:
        raise Exception(f"An error occurred while generating OTP: {str(e)}")