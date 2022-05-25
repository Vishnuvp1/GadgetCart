from twilio.rest import Client
from django.conf import settings

twilio_account_sid = settings.SECRET_KEY
twilio_auth_token = settings.AUTH_KEY
verification_sid = settings.VERIFICATION_KEY


client = Client(twilio_account_sid, twilio_auth_token)


def send_otp(phone_number):
    client.verify.services(verification_sid).verifications.create(
        to="+91" + phone_number, channel="sms"
    )


def verify_otp_number(phone_number, otp):
    try:
        verification_check = client.verify.services(
            verification_sid
        ).verification_checks.create(to="+91" + phone_number, code=otp)
        if verification_check.status == "approved":
            return True
    except:
        return False
