from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from foodproviders.models import PostCode
from postcode_latlng.convert import post_code_data_generator, LAT_KEY, LNG_KEY


def paged_iterator(qs, page_size):
    r = []
    for item in qs:
        r.append(item)
        if len(r) == page_size:
            yield r
            r = []
    yield r

class Command(BaseCommand):
    args = ''
    help = 'Load post codes'

    def handle(self, *args, **options):
        for lump in paged_iterator(post_code_data_generator("../data"), 500):
            post_codes = []
            for d in lump:
                post_code = d['Postcode']
                lat, lng = d[LAT_KEY], d[LNG_KEY]
                outward = post_code[:4].strip()
                inward = post_code[4:].strip()
                post_codes.append(PostCode(outward=outward, inward=inward,
                    location=Point(lat, lng)))
            PostCode.objects.bulk_create(post_codes)
