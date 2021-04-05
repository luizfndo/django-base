"""Module with view classes used in the thumbnail system."""
import os
from PIL import Image, ImageOps

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View
from django.core.files.storage import default_storage

from ..presets import PRESET_CHOICES, POSTER_SQUARED


class GeneratorView(View):
    """The Generator view class."""

    def get(self, request, path):
        """Handle the HTTP GET requests."""
        preset = request.GET.get('preset')
        return self.fit(os.path.join(settings.PHOTO_DIR, path), preset)

    def fit(self, image_url, preset):
        """Crops the image to be in the right aspect ratio."""
        preset_size = PRESET_CHOICES.get(preset, PRESET_CHOICES[POSTER_SQUARED])

        if default_storage.exists(image_url):
            response = HttpResponse(content_type='image/jpeg')
            with default_storage.open(image_url) as image_file:
                with Image.open(image_file) as image:
                    result = ImageOps.fit(image, preset_size, centering=(0.5, 0.5))
                    # image.thumbnail(preset_size, Image.ANTIALIAS)
                    # image.save(response, 'JPEG', quality=80, optimize=True, progressive=True)
                    result.save(response, 'JPEG', quality=80, optimize=True, progressive=True)
            return response
        return HttpResponseNotFound('Image not found.')
