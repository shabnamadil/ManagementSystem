import random


def generate_otp(length=6):
    otp_chars = "0123456789" 
    otp = ''.join(random.choice(otp_chars) for _ in range(length))
    return otp