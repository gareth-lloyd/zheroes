import re
from twilio.rest import TwilioRestClient

from django.conf import settings

from foodproviders.models import FoodProvider, PostCode
from smslink.models import PhoneUser

HELP_TEXT = "you messed up"
SMS_MAX_LEN = 160
POSTCODE_MATCHER = re.compile(r"([A-PR-UW-Z]{1}[A-IK-Y]?[0-9]?[A-HJKS-UW]?[ABEHMNPRVWXY]?|[0-9]?[0-9]?)\s?([0-9]{1}[ABD-HJLNP-UW-Z]{2})")
POSTCODE_MATCHER = re.compile(r"(([A-PR-UW-Z]{1}[A-IK-Y]?)([0-9]?[A-HJKS-UW]?[ABEHMNPRVWXY]?|[0-9]?[0-9]?))\s?([0-9]{1}[ABD-HJLNP-UW-Z]{2})")

def extract_post_code(text):
    results = POSTCODE_MATCHER.search(text.upper())
    if results:
        groups = results.groups()
        return groups[0], groups[-1]
    else:
        raise ValueError("no postcode supplied")

def send_sms(phone_user, text, num=None, total=None):
    if num and total:
        prepend = "{num}/{total}: ".format(num=num, total=total)
        if len(prepend) + len(text) <= SMS_MAX_LEN:
            text = prepend + text

    _do_send_sms(phone_user, text)

def _do_send_sms(phone_user, text):
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH)
    return client.sms.messages.create(body=text, to=phone_user.number,
            from_=settings.SMS_NUMBER)

def _do_send_sms(phone_user, text):
    print phone_user.number, text
    print


class Route(object):
    def __init__(self, phone_user, text):
        self.phone_user, self.text = phone_user, text

    def run(self):
        try:
            self._run()
        except Exception, e:
            print e
            UnknownRoute(self.phone_user, self.text)._run()


from django.template import Context, loader
def format_fp_for_sms(food_provider):
    t = loader.get_template('smslink/food_provider.txt')
    c = Context({'fp': food_provider})
    return t.render(c)


class HungryRoute(Route):
    def _run(self):
        outward, inward = extract_post_code(self.text)
        post_code = PostCode.objects.get(outward=outward, inward=inward)
        for i, fp in enumerate(FoodProvider.nearest_x(post_code, 3)):
            send_sms(self.phone_user, format_fp_for_sms(fp), i + 1, 3)

        self.send_follow_up()

    def send_follow_up(self):
        pass


class UnknownRoute(Route):
    def _run(self):
        send_sms(self.phone_user, HELP_TEXT)


def build_route(phone_user, text):
    if text.lower().strip().startswith('hungry'):
        route_type = HungryRoute
    else:
        route_type = UnknownRoute

    return route_type(phone_user, text)


def sms_received(number, text):
    try:
        phone_user = PhoneUser.objects.get(number=number)
    except PhoneUser.DoesNotExist:
        phone_user = PhoneUser.objects.create(number=number)

    route = build_route(phone_user, text)
    route.run()

