"""URL routes of the website application."""
from django.urls import path

from .views.home import HomeView


app_name = 'website'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]