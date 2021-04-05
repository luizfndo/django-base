"""This code capture events from models to attach functions to them."""
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User


@receiver(post_save, sender=User)
def document_post_save(sender, instance, created, **kwargs):
    """Tasks that should be executed after save an user.

    Everytime a new user is added, so we'll send a validation email.
    In the e-mail there is a link to validade the account of the user.
    """
    # pylint: disable=unused-argument
    if created:
        instance.send_validation_link()
