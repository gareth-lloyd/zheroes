from django import forms
from django.contrib.localflavor.uk.forms import UKPostcodeField

from foodproviders.models import FoodProvider, EntryRequirement
from foodproviders.api import age_to_entry_requirements

GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
)

class FoodProviderCriteriaForm(forms.Form):
    post_code = UKPostcodeField(required=True)
    age = forms.IntegerField(required=False)
    homeless = forms.BooleanField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    def food_providers(self):
        d = self.cleaned_data
        age, homeless, gender = d['age'], d['homeless'], d['gender']
        reqs = []
        if age:
            reqs.extend(age_to_entry_requirements(age))
        if homeless:
            reqs.append(EntryRequirement.objects.get(requirement="Homeless"))
        if gender == "male":
            reqs.append(EntryRequirement.objects.get(requirement="Men"))
        if gender == "female":
            reqs.append(EntryRequirement.objects.get(requirement="Women"))

        final_fps = []
        for fp in FoodProvider.objects.all().exclude(location=None):
            for req in fp.requirements.all():
                if req not in reqs:
                    break
            else:
                final_fps.append(fp)
        return final_fps
