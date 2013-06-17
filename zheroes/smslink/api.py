import re
from twilio.rest import TwilioRestClient

from django.conf import settings
from django.template import Context, loader

from foodproviders.models import FoodProvider, PostCode, EntryRequirement
from foodproviders.api import age_to_entry_requirements
from smslink.models import PhoneUser, SMS

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
    if len(text) > SMS_MAX_LEN:
        text = text[:SMS_MAX_LEN - 3] + '...'

    _do_send_sms(phone_user, text)

def _do_send_sms(phone_user, text):
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH)
    return client.sms.messages.create(body=text, to=phone_user.number,
            from_=settings.SMS_NUMBER)


class Route(object):
    def __init__(self, phone_user, text):
        self.phone_user, self.text = phone_user, text

    def run(self):
        try:
            self._run()
        except Exception, e:
            print e
            UnknownRoute(self.phone_user, self.text)._run()


def format_fp_for_sms(food_provider):
    t = loader.get_template('smslink/food_provider.txt')
    c = Context({'fp': food_provider})
    return t.render(c)


class HungryRoute(Route):
    SIGN_UP_PROMPT = "Would you like daily or weekly reminders of"\
        " food options in your area? Text back daily or weekly to"\
        " sign up."
    STOP_OPTION = "To stop these reminders, text back STOP"

    @staticmethod
    def route_match(text):
        return text.startswith('hungry')

    def _get_relevant_food_providers(self, post_code, num=3):
        if self.phone_user.requirements_satisfied.exists():
            # user has specified information about themselves
            fps = []
            for fp in FoodProvider.nearest_x(post_code, 10):
                if self.phone_user.meets_requirements(fp):
                    fps.append(fp)
                if len(fps) == num:
                    return fps
        else:
            return FoodProvider.nearest_x(post_code, num)

    def _run(self):
        outward, inward = extract_post_code(self.text)
        post_code = PostCode.objects.get(outward=outward, inward=inward)

        for fp in self._get_relevant_food_providers(post_code):
            send_sms(self.phone_user, format_fp_for_sms(fp))

        if not self.phone_user.update_frequency:
            send_sms(self.phone_user, self.SIGN_UP_PROMPT)
        else:
            send_sms(self.phone_user, self.STOP_OPTION)


class SignUpRoute(Route):
    NEXT_STEP_PROMPT = "Thanks! You're signed up. If you want,"\
            " you can tell us more about you so we can send you"\
            " good options. How old are you?"

    @staticmethod
    def route_match(text):
        return text.startswith('daily') or text.startswith('weekly')

    def _run(self):
        self.phone_user.update_frequency = 1 if self.text.startswith('daily') else 7
        self.phone_user.save()
        send_sms(self.phone_user, self.NEXT_STEP_PROMPT)

class AgeSubmittedRoute(Route):
    NEXT_STEP_PROMPT = "Thanks for that. Some food providers only"\
            " serve homeless people. Are you currently homeless?"\
            " Text back YES or NO."

    @staticmethod
    def route_match(text):
        return text.isdigit()

    def _run(self):
        age = int(self.text)
        for req in age_to_entry_requirements(age):
            self.phone_user.requirements_satisfied.add(req)
        send_sms(self.phone_user, self.NEXT_STEP_PROMPT)


class HomelessStatusSubmittedRoute(Route):
    NEXT_STEP_PROMPT = "Thanks for that. Some food providers serve"\
            " just men or just women. Are you male or female?"\
            " Text back MALE or FEMALE."
    YES = ('yes', 'y')
    NO = ('no', 'n')

    @staticmethod
    def route_match(text):
        return text in HomelessStatusSubmittedRoute.YES + HomelessStatusSubmittedRoute.NO

    def _run(self):
        if self.text in self.YES:
            req = EntryRequirement.objects.get(requirement='Homeless')
        else:
            req = EntryRequirement.objects.get(requirement='Not Homeless')
        self.phone_user.requirements_satisfied.add(req)
        send_sms(self.phone_user, self.NEXT_STEP_PROMPT)


class GenderSubmittedRoute(Route):
    COMPLETE_PROMPT = "Thanks! That's everything. Look out for food option"\
            " reminders in the future!"

    @staticmethod
    def route_match(text):
        return text == 'male' or text == 'female'

    def _run(self):
        if self.text == 'female':
            req, _ = EntryRequirement.objects.get_or_create(requirement='Women')
        else:
            req, _ = EntryRequirement.objects.get_or_create(requirement='Men')
        self.phone_user.requirements_satisfied.add(req)
        send_sms(self.phone_user, self.COMPLETE_PROMPT)


class UnknownRoute(Route):
    HELP_TEXT = "Sorry, I didn't understant that. Try again or text"\
            " HUNGRY and write a postcode to get food options nearby"

    @staticmethod
    def route_match(text):
        return True

    def _run(self):
        send_sms(self.phone_user, self.HELP_TEXT)


class StopRoute(Route):
    STOP_TEXT = "OK, you have stopped regular updates. You can text HUNGRY"\
            " and write a postcode to find out food options nearby at any time"

    @staticmethod
    def route_match(text):
        return text == 'stop'

    def _run(self):
        self.phone_user.update_frequency = 0
        self.phone_user.save()
        send_sms(self.phone_user, self.STOP_TEXT)


def preprocess_text(text):
    return text.lower().strip()

ROUTES = (HungryRoute, SignUpRoute, HomelessStatusSubmittedRoute,
        GenderSubmittedRoute, AgeSubmittedRoute, StopRoute, UnknownRoute)

def build_route(phone_user, text):
    text = preprocess_text(text)
    for route_type in ROUTES:
        if route_type.route_match(text):
            break
    return route_type(phone_user, text)


def sms_received(number, text):
    try:
        phone_user = PhoneUser.objects.get(number=number)
    except PhoneUser.DoesNotExist:
        phone_user = PhoneUser.objects.create(number=number)
    SMS.objects.create(phone_user=phone_user, text=text)

    route = build_route(phone_user, text)
    route.run()

