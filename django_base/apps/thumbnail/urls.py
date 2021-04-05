"""URL routes of the thumbnail application."""
from django.urls import re_path

from .views.generator import GeneratorView


app_name = 'thumbnail'

urlpatterns = [
    re_path(r'(?P<path>[\w.-]+)$', GeneratorView.as_view(), name='generator'),
]