import json
from django.views.generic import TemplateView
from django.http import HttpResponse

from foodproviders.models import EntryRequirement, DOTW
from foodproviders.api import unsatisfied_age_requirements, filter_food_providers
from foodproviders.templatetags.json_filters import ZheroesEncoder

class MapView(TemplateView):
    template_name = 'foodproviders/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['centreLat'] = 51.5171
        context['centreLng'] = -0.1062
        context['zoom'] = 11
        return context

def unsatisfied_requirements(query_dict):
    reqs = []
    age = query_dict.get('age')
    homeless = query_dict.get('homeless')
    gender = query_dict.get('gender')

    if age is not None:
        try:
            age = int(age)
            reqs.extend(unsatisfied_age_requirements(age))
        except:
            pass
    if homeless == 'false':
        reqs.append(EntryRequirement.objects.get(requirement='Homeless'))
    if gender == 'male':
        reqs.append(EntryRequirement.objects.get(requirement='Women'))
    if gender == 'female':
        reqs.append(EntryRequirement.objects.get(requirement='Men'))
    return reqs

def serving_time(query_dict):
    day = query_dict.get('day')
    if day not in [pair[0] for pair in DOTW]:
        day = None
    time = query_dict.get('time')
    if time not in ('breakfast', 'morning', 'lunch', 'afternoon', 'dinner'):
        time = None
    return day, time

def filter_fps(request):
    unsatisfied = unsatisfied_requirements(request.GET)
    day, time = serving_time(request.GET)

    fps = filter_food_providers(unsatisfied, day=day, time=time)

    content = json.dumps(fps, cls=ZheroesEncoder)
    return HttpResponse(content, content_type='application/json')

