from django import forms
from django.contrib.localflavor.uk.forms import UKPostcodeField

GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female')
)

class FoodProviderCriteriaForm(forms.Form):
    post_code = UKPostcodeField(required=True)
    age = forms.IntegerField(required=False)
    homeless = forms.BooleanField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
