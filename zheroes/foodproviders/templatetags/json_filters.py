from django.core.serializers import serialize, json
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.template import Library
from django.contrib.gis.geos import Point

from foodproviders.models import EntryRequirement, FoodProvider

register = Library()

def convert_food_provider(fp):
    return dict(
        id=fp.id,
        name=fp.name,
        cost=fp.get_cost_display().lower(),
        food_type=fp.get_food_type_display().lower(),
        organisation_type=fp.get_organisation_type_display().lower(),
        time=fp.time,
        requirements=list(fp.requirements.all()),
        referral_required=fp.referral_required,
        address=fp.address,
        location=fp.location,
        email=fp.email,
        website=fp.website,
        telephone=fp.telephone
    )

class ZheroesEncoder(json.DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        elif isinstance(o, FoodProvider):
            return convert_food_provider(o)
        elif isinstance(o, EntryRequirement):
            return o.get_requirement_display()
        elif isinstance(o, Point):
            return dict(x=o.x, y=o.y)
        else:
            return super(ZheroesEncoder, self).default(o)

def jsonify(object):
    return simplejson.dumps(object, cls=ZheroesEncoder)

register.filter('jsonify', jsonify)
jsonify.is_safe = True

