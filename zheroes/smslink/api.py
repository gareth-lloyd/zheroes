from twilio.rest import TwilioRestClient

from django.conf import settings

def send_sms(phone_user, text):
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH)
    return client.sms.messages.create(body=text, to=phone_user.number,
            from_=settings.SMS_NUMBER)
