from django.db import models

class PhoneUser(models.Model):
    number = models.CharField(max_length=20, db_index=True)
    post_code = models.ForeignKey('foodproviders.PostCode')

