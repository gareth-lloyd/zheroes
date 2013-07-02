import json
from django.views.generic import TemplateView
from django.http import HttpResponse

from foodproviders.forms import FoodProviderCriteriaForm
from foodproviders.templatetags.json_filters import ZheroesEncoder

class MapView(TemplateView):
    template_name = 'foodproviders/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['centreLat'] = 51.5171
        context['centreLng'] = -0.1062
        context['zoom'] = 11
        return context

def filter_food_providers(request):
    form = FoodProviderCriteriaForm(request.GET)
    content = json.dumps(form.food_providers(), cls=ZheroesEncoder)
    return HttpResponse(content, content_type="application/json")

