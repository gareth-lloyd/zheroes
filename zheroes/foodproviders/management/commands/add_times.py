import csv

from django.core.management.base import BaseCommand

from foodproviders.models import (FoodProvider, ServingTime)
D = {
    'friday': 'f',
    'monday': 'm',
    'saturday': 's',
    'sunday': 'S',
    'thursday': 'T',
    'tuesday': 't',
    'wednesday': 'w',
}

TIMES = ('breakfast', 'morning', 'lunch', 'afternoon', 'dinner')


class Command(BaseCommand):
    args = ''
    help = 'Load food provider opening times'

    def handle(self, *args, **kwargs):
        with open('foodproviders/data/f208730.csv', 'rb') as f:
            reader = csv.DictReader(f)
            for line in reader:
                id_ = line['code']
                fp = FoodProvider.objects.get(pk=id_)
                for day in D.keys():
                    db_day = D[day]
                    s, _ = ServingTime.objects.get_or_create(provider=fp, day=db_day)
                    for val in line[day].split('\n'):
                        for time in TIMES:
                            if val.startswith(time):
                                setattr(s, time, True)
                    s.save()
        for s in ServingTime.objects.all():
            if any(getattr(s, t) for t in TIMES):
                continue
            else:
                s.delete()

