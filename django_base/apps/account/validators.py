import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


from . import models


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[\w-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and -/_ characters.'
    )
    flags = 0


@deconstructible
class RepetitiveValidator(validators.RegexValidator):
    regex = r'^.*(.)\1{2}.*$'
    inverse_match = True
    message = _('Too many repeating characters.')
    flags = 0


@deconstructible
class UsernameBlacklistValidator:
    """Validator of usernames.

    Some usernames are reserved or cannot be used for security reasons. That
    usernames are stored in the UsernameBlacklist model.
    """

    def __call__(self, value):
        """Magic method call."""
        model = models.UsernameBlacklist
        if model.objects.filter(username=value).exists():
            raise ValidationError(_('Invalid username'), code='invalid')
