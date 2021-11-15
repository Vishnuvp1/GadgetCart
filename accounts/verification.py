from twilio.rest import Client


twilio_account_sid = 'ACd939105454ca82283f00583000ea62d2'
twilio_auth_token = '54c75c0013f7af4420ba22bdda4b10e4'
verification_sid = 'VA2f29e15c44299f5544304c8bc6de12d8'

client = Client(twilio_account_sid, twilio_auth_token)

def send_otp(phone_number):
    client.verify.services(verification_sid).verifications.create(to='+91' + phone_number, channel='sms')


def verify_otp_number(phone_number, otp):
    try:
        verification_check = client.verify.services(verification_sid).verification_checks.create(
            to='+91' + phone_number, code=otp)
        if verification_check.status == 'approved':
            return True
    except:
        return False
