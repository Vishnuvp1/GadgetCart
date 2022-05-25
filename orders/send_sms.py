import os
from django.conf import settings
from twilio.rest import Client


account_sid = settings.SECRET_KEY
auth_token = settings.AUTH_KEY
client = Client(account_sid, auth_token)


def send_sms():
    message = client.messages.create(
        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
        from_="+15017122661",
        to="+918111838707",
    )

    print("Message sent successfully")
