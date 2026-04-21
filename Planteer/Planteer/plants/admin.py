from django.contrib import admin
from .models import Plant, Commint, Country


class PlantAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_edible", "created_at"]
    list_filter = ["category", "is_edible"]

class CommintAdmin(admin.ModelAdmin):
    list_display = ["name", "plant", "created_at"]
    list_filter = ["plant"]

class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Plant, PlantAdmin)
admin.site.register(Commint, CommintAdmin)
admin.site.register(Country, CountryAdmin)