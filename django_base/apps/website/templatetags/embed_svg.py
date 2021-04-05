"""Module with custom embed_svg tag."""
from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe
from django.contrib.staticfiles import finders


register = Library()


class SVGNotFound(Exception):
    """Exception raised when the SVG was not found."""


@register.simple_tag
def embed_svg(filename):
    """Returns the SVG source code to be embed in the HTML.

    The appname allows to embed SVG files from other apps of the project.
    """
    if not settings.DEBUG:
        parts = filename.split('/')
        parts.insert(1, 'build')
        filename = '/'.join(parts)

    path = finders.find(filename, all=True)

    if not path:
        message = f'{filename} not found.'
        if settings.DEBUG:
            raise SVGNotFound(message)
        else:
            logger.warning(message)
            return ''
    if isinstance(path, (list, tuple)):
        path = path[0]
    with open(path) as svg_file:
        svg = mark_safe(svg_file.read())
    return svg