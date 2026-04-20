from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('messages/', views.contact_messages_view, name='messages'),
]