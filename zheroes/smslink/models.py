from django.db import models

class PhoneUser(models.Model):
    number = models.CharField(max_length=20, db_index=True)
    post_code = models.ForeignKey('foodproviders.PostCode', blank=True, null=True)
    last_contacted = models.DateTimeField(blank=True, null=True)

    requirements_satisfied = models.ManyToManyField('foodproviders.EntryRequirement')
    update_frequency = models.IntegerField(default=0)

    def meets_requirements(self, food_provider):
        requirements_satisfied = self.requirements_satisfied.all()
        for requirement in food_provider.requirements.all():
            if not requirement in requirements_satisfied:
                return False
        return True

class SMS(models.Model):
    phone_user = models.ForeignKey(PhoneUser)
    text = models.CharField(max_length=170)
