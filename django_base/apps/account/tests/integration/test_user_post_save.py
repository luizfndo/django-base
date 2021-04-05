"""Unit test of user model and signals"""
from model_mommy import mommy

from django.core import mail
from django.test import TestCase

from django_base.apps.account.models import User
from django_base.apps.account.dispatch import document_post_save


class TestUserPostSaveView(TestCase):
    """Test signal post_save sent from User model"""

    def test_validation_link_on_create(self):
        """Test it was sent a validation link after create an user.

        Every time a new user is add then the system send a validation link
        to check the e-mail account and avoid spam.
        """
        user = mommy.make(User)
        user.set_password(user.password)
        user.save()

        mail.outbox = []

        document_post_save(None, user, True)
        self.assertIn(user.email, mail.outbox[0].to)
        # pylint: disable=deprecated-method
        self.assertRegex(str(mail.outbox[0].body), user.get_validation_link())

    def test_validation_link_on_update(self):
        """Test if account validation will be skipped when updating user data.

        We should skip sending the validation link on the data updates. Even
        when the account was not verified yet.
        """
        user = mommy.make(User)
        user.set_password(user.password)
        user.save()

        mail.outbox = []
        document_post_save(None, user, False)
        self.assertEqual(len(mail.outbox), 0)
