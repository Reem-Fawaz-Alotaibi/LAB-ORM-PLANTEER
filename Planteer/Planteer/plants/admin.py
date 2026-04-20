from django.contrib import admin
from .models import Plant,Commint

class PlantAdmin(admin.ModelAdmin):
    list_display =["plant","name","comment"]
    list_filter =["plant","name"]

admin.site.register(Plant)
admin.site.register(Commint,PlantAdmin)