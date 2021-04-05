"""Module with test cases of the Account Recovery view."""
from model_mommy import mommy
from django.urls import reverse
from django.test import TestCase, Client, tag

from django_base.apps.account.models import User


@tag('integration')
class TestAccountRecoveryView(TestCase):
    """Test cases of the Account Recovery view."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.client = Client()

    def test_account_recovery(self):
        """Tests account recovery link."""
        user = mommy.prepare(User)
        user_pass = user.password
        user.set_password(user.password)
        user.save()

        # Get the account recovery link.
        link_recovery = user.get_recovery_link(absolute=False)

        # Delete user account.
        user.delete()
        self.assertIsNotNone(user.deleted)

        # Recovery the user account.
        response = self.client.get(link_recovery, follow=True)
        user.refresh_from_db()
        self.assertIsNone(user.deleted)
        self.assertTemplateUsed(response, 'account/recovery-done.html')
