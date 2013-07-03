from foodproviders.models import (EntryRequirement, FoodProvider, ServingTime,
        FOOD_TYPE_GROUPS)


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

def filter_food_providers(unsatisfied_reqs, day=None, time=None, food_type=None):
    fp_kwargs = {'location__isnull': False}

    if day or time:
        serving_kwargs = {}
        if day:
            serving_kwargs['day'] = day
        if time:
            serving_kwargs[time] = True
        fp_kwargs['id__in'] = ServingTime.objects.filter(**serving_kwargs)\
                .values_list('provider__id', flat=True)

    if food_type and food_type in FOOD_TYPE_GROUPS:
        fp_kwargs['food_type__in'] = FOOD_TYPE_GROUPS[food_type]


    fps = FoodProvider.objects.filter(**fp_kwargs)
    fps = fps.exclude(location=None).select_related('requirements')


    final_fps = []
    for fp in fps:
        for req in fp.requirements.all():
            if req in unsatisfied_reqs:
                break
        else:
            final_fps.append(fp)
    return final_fps

