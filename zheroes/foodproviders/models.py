from django.contrib.gis.db import models
from django.template import Context, loader

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
    ('M', 'Cooked meal and food parcel'),
    ('p', 'Cooked meal parcel'),
    ('f', 'Milk, fruit and vegetable'),
)
FOOD_TYPE_GROUPS = {
    'parcel': ['n', 'M', 'p', 'f'],
    'meal': ['c', 's', 'm', 'M', 'p']
}

ENTRY_REQS = (
    ('Mental health','You must be diagnosed with a mental health issue'),
    ('Families','You must have a family'),
    ('Fixed address','You must have a fixed address'),
    ('Ex service men','You must be an ex-serviceman or woman'),
    ('Ethnic identity','You must belong to a particular ethnic group - enquire for further details'),
    ('Right to work in UK','You must have the right to work in UK'),
    ('Refugees, asylum seekers, migrants','This group is for refugees, asylum seekers, and migrants'),
    ('Homeless','This service caters for homeless people only'),
    ('In receipt of a benefit','You must be in receipt of a benefit'),
    ('Under 25','You must be under 25'),
    ('Over 25','You must be over 25'),
    ('Over 60','You must be over 60'),
    ('Over 16','You must be over 16'),
    ('Live in area','You must live in the area'),
    ('Women','This service caters for women only'),
)

class PostCode(models.Model):
    outward = models.CharField(max_length=5, db_index=True)
    inward = models.CharField(max_length=5)

    location = models.PointField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        unique_together = ('outward', 'inward')

    def __unicode__(self):
        return u"{out} {in_}".format(out=self.outward, in_=self.inward)

class EntryRequirement(models.Model):
    requirement = models.CharField(max_length=64, choices=ENTRY_REQS,
            unique=True)

    def __unicode__(self):
        return self.requirement


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
    referral_required = models.BooleanField(default=False)

    address = models.CharField(max_length=256)
    location = models.PointField(blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    website = models.CharField(max_length=256, blank=True, null=True)
    telephone = models.CharField(max_length=256, blank=True, null=True)

    objects = models.GeoManager()

    @staticmethod
    def _annotated():
        return FoodProvider.objects\
                .annotate(num_requirements=models.Count('requirements'))

    @staticmethod
    def open_access():
        return FoodProvider._annotated().filter(num_requirements=0)

    @staticmethod
    def restricted():
        return FoodProvider._annotated().filter(num_requirements__gt=0)

    @staticmethod
    def nearest_x(post_code, x):
        return FoodProvider.objects.all().distance(post_code.location).order_by('distance')[:x]

    def description_as_html(self):
        t = loader.get_template('foodproviders/food_provider_description.html')
        c = Context({'fp': self})
        return t.render(c)

    def __unicode__(self):
        return self.name

DOTW = (
    ('m', 'Monday'),
    ('t', 'Tuesday'),
    ('w', 'Wednesday'),
    ('T', 'Thursday'),
    ('f', 'Friday'),
    ('s', 'Saturday'),
    ('S', 'Sunday'),
)

class ServingTime(models.Model):
    day = models.CharField(max_length=1, choices=DOTW)
    provider = models.ForeignKey(FoodProvider)

    breakfast = models.BooleanField(default=False,
            help_text="early morning 'til 9am")
    morning = models.BooleanField(default=False,
            help_text="9am 'til 12 noon")
    lunch = models.BooleanField(default=False,
            help_text="12 noon 'til 2pm")
    afternoon = models.BooleanField(default=False,
            help_text="2pm 'til 5pm")
    dinner = models.BooleanField(default=False,
            help_text="5pm onwards")

    def __unicode__(self):
        base = "{d}: ".format(d=self.day)
        times = []
        for t in ('breakfast', 'morning', 'lunch', 'afternoon', 'dinner'):
            if getattr(self, t):
                times.append(t)
        return base + ", ".join(times)

    class Meta:
        unique_together = ('day', 'provider')


