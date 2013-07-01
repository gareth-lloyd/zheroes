from django.views.generic.edit import FormView

from foodproviders.forms import FoodProviderCriteriaForm
from foodproviders.models import FoodProvider, PostCode

class MapView(FormView):
    form_class = FoodProviderCriteriaForm
    template_name = 'foodproviders/map.html'

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def _entry_requirements_from_form(self, form):
        pass

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        form = kwargs['form']
        if form.is_bound and form.is_valid():
            outward, inward = form.cleaned_data['post_code'].split()
            post_code = PostCode.objects.get(outward=outward, inward=inward)
            context['centreLat'] = post_code.location.x
            context['centreLng'] = post_code.location.y
            context['zoom'] = 13
            context['fps'] = form.food_providers()
        else:
            context['centreLat'] = 51.5171
            context['centreLng'] = -0.1062
            context['zoom'] = 11
            context['open_fps'] = FoodProvider.open_access().exclude(location=None)
            context['restricted_fps'] = FoodProvider.restricted().exclude(location=None)
        return context

