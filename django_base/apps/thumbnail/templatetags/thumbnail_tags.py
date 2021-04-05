"""Module with the template tags used by the thumbnail application."""
import os

from django.template import Library
from django.urls import reverse


register = Library()


@register.simple_tag
def thumbnail_url(path, profile):
    path = os.path.basename(path)
    url = reverse('thumbnail:generator', args=(path,))
    return f'{url}?preset={profile}'