from django import forms
from django.contrib.localflavor.uk.forms import UKPostcodeField

from foodproviders.models import FoodProvider, EntryRequirement, DOTW
from foodproviders.api import age_to_entry_requirements

GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
)
SERVING_TIMES = (
    ('b', 'Breakfast'),
    ('m', 'Morning'),
    ('l', 'Lunch'),
    ('a', 'Afternoon'),
    ('d', 'Dinner'),
)

class FoodProviderCriteriaForm(forms.Form):
    post_code = UKPostcodeField(required=True)
    age = forms.IntegerField(required=False)
    homeless = forms.BooleanField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    day = forms.ChoiceField(choices=DOTW)
    serving_time = forms.ChoiceField(choices=SERVING_TIMES)

    def _requirements(self):
        reqs = []
        if self.is_bound and self.is_valid():
            d = self.cleaned_data
            age, homeless, gender = d['age'], d['homeless'], d['gender']
            if age:
                reqs.extend(age_to_entry_requirements(age))
            if homeless:
                reqs.append(EntryRequirement.objects.get(requirement="Homeless"))
            if gender == "male":
                reqs.append(EntryRequirement.objects.get(requirement="Men"))
            if gender == "female":
                reqs.append(EntryRequirement.objects.get(requirement="Women"))
        return reqs

    def food_providers(self):
        final_fps = []
        reqs = self._requirements()
        for fp in FoodProvider.objects.all().exclude(location=None):
            for req in fp.requirements.all():
                if req not in reqs:
                    break
            else:
                final_fps.append(fp)
        return final_fps
