from django.contrib.gis.db import models

# Create your models here.

ORG_TYPES = ()

class PostCode(models.Model):
    outward = models.CharField(max_length=5)
    inward = models.CharField(max_length=5)

    location = models.PointField(blank=True, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return u"{out} {in_}".format(out=self.outward, in_=self.inward)


class FoodProvider(models.Model):
    zheroes_id = models.IntField()
    name = models.CharField(max_length=256)
    cost = models.CharField(max_length=128)

    means_of_entry = models.TextField(blank=True, null=True)
    organisation_type = models.CharField(choices=ORG_TYPES)
    post_code = models.ForeignKey(PostCode, blank=True)

"Food type"
"Pathway/means of entry"
"Elegibility"
"Location"
"Time"
"Email/Website"
"Telephone number"
