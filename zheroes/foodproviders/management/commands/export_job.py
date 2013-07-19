from django.core.management.base import BaseCommand

from foodproviders.models import (FoodProvider, EntryRequirement, ORG_TYPES,
        FOOD_TYPES, FOOD_COSTS, ENTRY_REQS, PostCode)


class Command(BaseCommand):
    args = ''
    help = 'Export food provider times'

    def handle(self, *args, **kwargs):
        with open('output.csv', 'w') as f:
            for fp in FoodProvider.objects.all():
                if not fp.time.lower().startswith('n/a'):
                    f.write('"%d", "%s"\n' % (fp.id, fp.time.encode('utf-8')))
