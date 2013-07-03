import csv, re

from django.core.management.base import BaseCommand

from foodproviders.models import (FoodProvider, EntryRequirement, ORG_TYPES,
        FOOD_TYPES, FOOD_COSTS, ENTRY_REQS, PostCode)

POSTCODE_MATCHER = re.compile("([A-PR-UWYZ][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {0,1}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)")

ID = "ID Number"
ORG = "Organisation"
UJS = ("User Journey1", "User Journey2", "User Journey3", "User Journey4",
            "User Journey5")
ORG_TYPE = "Organisation Type"
COST = "Food Cost"
FOOD_TYPE = "Food type"
PATH = "Pathway/means of entry"
EL = "Elegibility"
LOC = "Location"
TIME = "Time"
EM_WB = "Email/Website"
TEL = "Telephone number"

FRONTLINE = "Referral through frontline services"

def _lookup_table(choices):
    return {c[1]: c[0] for c in choices}

def get_post_code(post_code_str):
    if not post_code_str:
        return None
    outward, inward = post_code_str.split()
    return PostCode.objects.get(outward=outward, inward=inward)

class Command(BaseCommand):
    args = ''
    help = 'Load food providers'

    def handle(self, *args, **kwargs):
        try:
            FoodProvider.objects.all().delete()

            ORG_TYPE_LOOKUP = _lookup_table(ORG_TYPES)
            FOOD_COST_LOOKUP = _lookup_table(FOOD_COSTS)
            FOOD_TYPE_LOOKUP = _lookup_table(FOOD_TYPES)
            ENTRY_LOOKUP = _lookup_table(ENTRY_REQS)

            zheroes_id = None
            with open('foodproviders/data/food_sources.csv', 'rb') as f:
                reader = csv.DictReader(f)
                for d in reader:
                    post_codes = POSTCODE_MATCHER.search(d['Location'])
                    post_code = get_post_code(post_codes.groups()[0] if post_codes else None)

                    email_web = d[EM_WB]
                    email = email_web if '@' in email_web else None
                    website = email_web if '@' not in email_web else None

                    zheroes_id = int(d[ID]) if d[ID] else zheroes_id
                    path=d[PATH]
                    referral = path.startswith(FRONTLINE)

                    prov = FoodProvider.objects.create(
                            zheroes_id=zheroes_id,
                            name=d[ORG],
                            cost=FOOD_COST_LOOKUP[d[COST]],
                            food_type=FOOD_TYPE_LOOKUP[d[FOOD_TYPE]],
                            organisation_type=ORG_TYPE_LOOKUP[d[ORG_TYPE]],
                            time=d[TIME],
                            means_of_entry=path,
                            referral_required=referral,
                            eligibility=d[EL],
                            address=d[LOC],
                            location=post_code.location if post_code else None,
                            email=email,
                            website=website,
                            telephone=d[TEL]
                    )
                    for key in UJS:
                        requirement = d[key]
                        if requirement and requirement in ENTRY_LOOKUP:
                            r, _ = EntryRequirement.objects.get_or_create(
                                    requirement=requirement)
                            prov.requirements.add(r)

        except Exception, e:
            print e
