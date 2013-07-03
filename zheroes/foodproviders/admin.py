from django.contrib.gis import admin
from foodproviders.models import FoodProvider, EntryRequirement, ServingTime

class ServingTimeInline(admin.TabularInline):
    model = ServingTime

class EntryRequirementAdmin(admin.ModelAdmin):
    pass
admin.site.register(EntryRequirement, EntryRequirementAdmin)

class FoodProviderAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [ServingTimeInline]
admin.site.register(FoodProvider, FoodProviderAdmin)


