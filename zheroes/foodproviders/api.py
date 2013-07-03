from foodproviders.models import EntryRequirement, FoodProvider, ServingTime


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

def filter_food_providers(unsatisfied_reqs, day=None, time=None):
    final_fps = []
    if day or time:
        kwargs = {}
        if day:
            kwargs['day'] = day
        if time:
            kwargs[time] = True
        fp_ids = ServingTime.objects.filter(**kwargs).values_list('provider__id', flat=True)
        fps = FoodProvider.objects.filter(id__in=fp_ids)
    else:
        fps = FoodProvider.objects.all()
    fps = fps.exclude(location=None).select_related('requirements')
    for fp in fps:
        for req in fp.requirements.all():
            if req in unsatisfied_reqs:
                break
        else:
            final_fps.append(fp)
    return final_fps

