"""Module with custom inline_css tag."""
import os

from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe


register = Library()


class CSSNotFound(Exception):
    """Exception raised when the CSS was not found."""


@register.simple_tag
def inline_css(css_file):
    """Puts the CSS code inline in the HTML file."""
    app_name = 'design'
    static_url = settings.STATIC_URL

    file_path, file_name = os.path.split(css_file)
    file_name, ext = os.path.splitext(file_name)

    files = {
        os.path.join(app_name, file_path, f'{file_name}.min{ext}'),
        os.path.join(app_name, css_file)
    }

    for _file in files:
        result = finders.find(_file, all=True)
        if result:
            if isinstance(result, (list, tuple)):
                result = result[0]
            with open(result) as css_file:
                css = mark_safe(css_file.read())

            if not settings.DEBUG:
                static_url = f'https://{settings.STATIC_CUSTOM_DOMAIN}'

            css = css.replace('{{static}}', static_url.rstrip('/'))

            return mark_safe(f'<style media="screen">{css}</style>')
    else:
        message = 'The {} file was not found by the inline_css tag.'.format(
            files[1] # The original file (not minified).
        )

        if settings.DEBUG:
            raise CSSNotFound(message)
        else:
            logger.warning(message)
            return ''