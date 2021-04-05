"""Module with app configurations."""
from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class AccountConfig(AppConfig):
    """Account app configurations."""
    name = 'django_base.apps.account'
    verbose_name = pgettext_lazy('App name', 'Account')

    def ready(self):
        """Called when the app is ready."""
        # pylint: disable=unused-variable
        # from . import dispatch
