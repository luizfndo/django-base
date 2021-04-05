"""Module with tests of the sign up done view."""
from model_mommy import mommy
from django.urls import reverse
from django.test import TestCase, Client, tag

from django_base.apps.account.models import User


@tag('integration')
class TestSignupDoneView(TestCase):
    """Test cases of the Sign Up Done view."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.home = reverse('home')
        self.endpoint = reverse('account:sign-up-done')
        self.client = Client()

    def test_redirect_when_non_logged(self):
        """Tests whether the user will be properly redirected.

        When the user enter in the sign up done page and is not logged, so
        the user must to be reditected to the homepage.
        """
        response = self.client.get(self.endpoint)
        self.assertRedirects(response, self.home)

    def test_redirect_when_verified(self):
        """Tests whether the user will be properly redirected.

        When the user enter in the sign up done page and is logged, so
        the user must to be reditected to the homepage.
        """
        user = mommy.make(User)
        user_pass = user.password
        user.set_password(user_pass)
        user.is_verified = True
        user.save()

        logged = self.client.login(username=user.username, password=user_pass)
        self.assertTrue(logged)

        response = self.client.get(self.endpoint)
        self.assertRedirects(response, self.home)

    def test_signup_done_view(self):
        """Tests whether the user will see the properly page after sign up.

        After Sign Up the user should see the Sign Up Done page.
        """
        user = mommy.make(User)
        user_pass = user.password
        user.set_password(user_pass)
        user.save()

        logged = self.client.login(username=user.username, password=user_pass)
        self.assertTrue(logged)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
