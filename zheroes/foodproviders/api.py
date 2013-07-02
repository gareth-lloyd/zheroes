from foodproviders.models import EntryRequirement, FoodProvider


def age_to_entry_requirements(age):
    reqs = []
    if age > 16:
        reqs.append(EntryRequirement.objects.get(requirement="Over 16"))
    if age < 25:
        reqs.append(EntryRequirement.objects.get(requirement="Under 25"))
    if age >= 25:
        reqs.append(EntryRequirement.objects.get(requirement="Over 25"))
    if age > 60:
        reqs.append(EntryRequirement.objects.get(requirement="Over 60"))
    return reqs

def unsatisfied_age_requirements(age):
    reqs = []
    if age < 16:
        reqs.append(EntryRequirement.objects.get(requirement="Over 16"))
    if age > 25:
        reqs.append(EntryRequirement.objects.get(requirement="Under 25"))
    if age <= 25:
        reqs.append(EntryRequirement.objects.get(requirement="Over 25"))
    if age < 60:
        reqs.append(EntryRequirement.objects.get(requirement="Over 60"))
    return reqs

def filter_food_providers(unsatisfied_reqs):
    final_fps = []
    fps = FoodProvider.objects.all().select_related('requirements')
    fps = fps.exclude(location=None)
    for fp in fps:
        for req in fp.requirements.all():
            if req in unsatisfied_reqs:
                break
        else:
            final_fps.append(fp)
    return final_fps
