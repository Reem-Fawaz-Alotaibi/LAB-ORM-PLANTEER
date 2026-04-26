from django.contrib import admin
from .models import Plant, Comment, Country


class PlantAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_edible", "created_at"]
    list_filter = ["category", "is_edible"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "plant", "created_at"]
    list_filter = ["plant"]

class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Plant, PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Country, CountryAdmin)