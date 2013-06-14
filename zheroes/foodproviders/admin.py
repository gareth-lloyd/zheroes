from django.contrib.gis import admin
from foodproviders.models import FoodProvider, EntryRequirement


class EntryRequirementAdmin(admin.ModelAdmin):
    pass
admin.site.register(EntryRequirement, EntryRequirementAdmin)

class FoodProviderAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(FoodProvider, FoodProviderAdmin)


