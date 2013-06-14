from django.views.generic.edit import FormView

from foodproviders.forms import FoodProviderCriteriaForm
from foodproviders.models import FoodProvider, PostCode, EntryRequirement
from foodproviders.api import age_to_entry_requirements

class MapView(FormView):
    form_class = FoodProviderCriteriaForm
    template_name = 'foodproviders/map.html'

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def _entry_requirements_from_form(self, form):
        pass

    def food_providers_from_form(self, form):
        d = form.cleaned_data
        age, homeless, gender = d['age'], d['homeless'], d['gender']
        reqs = []
        if age:
            reqs.extend(age_to_entry_requirements(age))
        if homeless:
            reqs.append(EntryRequirement.objects.get(requirement="Homeless"))
        if gender == "male":
            reqs.append(EntryRequirement.objects.get(requirement="Men"))
        if gender == "female":
            reqs.append(EntryRequirement.objects.get(requirement="Women"))

        final_fps = []
        for fp in FoodProvider.objects.all().exclude(location=None):
            for req in fp.requirements.all():
                if req not in reqs:
                    break
            else:
                final_fps.append(fp)
        return final_fps

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        form = kwargs['form']
        if form.is_bound and form.is_valid():
            outward, inward = form.cleaned_data['post_code'].split()
            post_code = PostCode.objects.get(outward=outward, inward=inward)
            context['centreLat'] = post_code.location.x
            context['centreLng'] = post_code.location.y
            context['zoom'] = 13
            context['fps'] = self.food_providers_from_form(form)
        else:
            context['centreLat'] = 51.5171
            context['centreLng'] = -0.1062
            context['zoom'] = 11
            context['fps'] = FoodProvider.objects.all().exclude(location=None)
        print len(context['fps'])
        return context

