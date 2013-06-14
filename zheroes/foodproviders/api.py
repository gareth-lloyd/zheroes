from foodproviders.models import EntryRequirement

def age_to_entry_requirements(age):
    reqs = []
    if age > 16:
        reqs.append(EntryRequirement.objects.get(requirement="Over 16"))
    if age < 25:
        reqs.append(EntryRequirement.objects.get(requirement="Under 25"))
    if age > 25:
        reqs.append(EntryRequirement.objects.get(requirement="Over 25"))
    if age > 60:
        reqs.append(EntryRequirement.objects.get(requirement="Over 60"))
    return reqs
