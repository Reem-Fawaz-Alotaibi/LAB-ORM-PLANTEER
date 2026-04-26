from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('all/', views.all_plants_view, name='all_plants'),
    path('new/', views.new_plant_view, name='new_plant'),
    path('search/', views.search_plants_view, name='search_plants'),
    path('<int:plant_id>/detail/', views.plant_detail_view, name='plant_detail'),
    path('<int:plant_id>/update/', views.update_plant_view, name='update_plant'),
    path('<int:plant_id>/delete/', views.delete_plant_view, name='delete_plant'),
    path('<int:plant_id>/comment/', views.add_comment_view, name='add_comment_view'),
    path('country/<int:country_id>/', views.country_plants_view, name='country_plants'),
]