"""Module with test cases of the Account Delete view."""
from model_mommy import mommy
from django.urls import reverse
from django.test import TestCase, Client, tag

from django_base.apps.account.models import User


@tag('integration')
class TestAccountDeleteView(TestCase):
    """Test cases of the Account Delete view."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.client = Client()

    def test_delete_authenticated_user(self):
        """Tests delete authenticated user."""
        user = mommy.prepare(User)
        user_pass = user.password
        user.set_password(user.password)
        user.save()

        # Ensure the user is logically visible / non-excluded.
        self.assertIsNone(user.deleted)

        logged = self.client.login(username=user.username, password=user_pass)
        self.assertTrue(logged)
        self.assertTrue(user.is_authenticated)

        endpoint = reverse('account:delete')
        response = self.client.post(endpoint)

        # After being deleted, the user should logout.
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # The user cannot be retrieve because it was logically excluded.
        with self.assertRaises(User.DoesNotExist):
            user.refresh_from_db()

        self.assertTemplateUsed(response, 'account/account_delete_done.html')

    def test_delete_unauthenticated_user(self):
        """Tests delete unauthenticated user.

        In this case the user is an AnonymousUser. The browser should be
        redirect to the login page.
        """
        endpoint = reverse('account:delete')
        response = self.client.post(endpoint, follow=True)
        self.assertRedirects(response, reverse('account:login'))
