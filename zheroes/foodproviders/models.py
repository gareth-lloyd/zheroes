from django.contrib.gis.db import models
from django.contrib.gis.measure import Distance

FOOD_COSTS = (
    ('f', 'Free'),
    ('l', 'Low cost'),
    ('m', 'Free and low cost'),
)

ORG_TYPES = (
    ('b', 'food bank'),
    ('c', 'Church/Christian organistaion'),
    ('d', 'Day centre/drop in'),
    ('f', 'Food distribution'),
    ('h', 'Hostel/shelter'),
    ('y', 'Children and young peoples organistion'),
    ('s', 'Surplus food organistion'),
    ('r', 'Restaurant/cafe'),
    ('o', 'Other'),
    ('H', 'Homeless organistion'),
    ('i', 'Social improvement organisation'),
    ('S', 'Social club'),
    ('g', 'Government initiative'),
    ('R', 'Religious organisation'),
    ('t', 'Theatre company'),
    ('m', 'Mosque'),
    ('c', 'community'),
    ('e', 'food enterprise'),
)

FOOD_TYPES = (
    ('c', 'Cooked meal'),
    ('n', 'Non perishable/food parcel'),
    ('s', 'Soup/Sandwiches'),
    ('m', 'Mixed cooked and cold food'),
    ('t', 'Tea run'),
    ('m', 'Cooked meal and food parcel'),
    ('p', 'Cooked meal parcel'),
    ('f', 'Milk, fruit and vegetable'),
)

ENTRY_REQS = (
    ('m','Mental health'),
    ('f','Families'),
    ('o','Over 25'),
    ('a','Fixed address'),
    ('x','Ex service men'),
    ('u','Under 25'),
    ('e','Ethnic identity'),
    ('O','Over 60'),
    ('r','Right to work in UK'),
    ('R','Refugees, asylum seekers, migrants'),
    ('h','Homeless'),
    ('i','In receipt of a benefit'),
    ('v','Over 16'),
    ('l','Live in area'),
    ('w','Women'),
)

class PostCode(models.Model):
    outward = models.CharField(max_length=5)
    inward = models.CharField(max_length=5)

    location = models.PointField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        unique_together = ('outward', 'inward')

    def __unicode__(self):
        return u"{out} {in_}".format(out=self.outward, in_=self.inward)

class EntryRequirement(models.Model):
    requirement = models.CharField(max_length=2, choices=ENTRY_REQS,
            unique=True)

class FoodProvider(models.Model):
    zheroes_id = models.IntegerField()
    name = models.CharField(max_length=256)

    cost = models.CharField(max_length=2, choices=FOOD_COSTS)
    food_type = models.CharField(max_length=2, choices=FOOD_TYPES)
    organisation_type = models.CharField(max_length=2, choices=ORG_TYPES)
    time = models.CharField(max_length=512, blank=True, null=True)

    means_of_entry = models.CharField(max_length=512, blank=True, null=True)
    eligibility = models.CharField(max_length=512, blank=True, null=True)
    requirements = models.ManyToManyField(EntryRequirement)

    address = models.CharField(max_length=256)
    post_code = models.ForeignKey(PostCode, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    website = models.CharField(max_length=256, blank=True, null=True)
    telephone = models.CharField(max_length=256, blank=True, null=True)

    @staticmethod
    def near_post_code(post_code, km=1):
        d = Distance(km=km)
        post_codes = PostCode.objects.filter(location__distance_lte=(post_code.location, d))
        fps = FoodProvider.objects.filter(post_code__in=list(post_codes))
        return fps

