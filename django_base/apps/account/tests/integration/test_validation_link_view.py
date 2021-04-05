"""Module with tests of the Validation Link View."""
from model_mommy import mommy
from django.urls import reverse
from django.test import TestCase, Client, tag

from django_base.apps.account.models import User


@tag('integration')
class TestValidationLinkView(TestCase):
    """Test cases of the Validation Link View."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.client = Client()
        self.user = mommy.make(User)
        self.user.set_password(self.user.password)
        self.user.save()

    def test_validation_link_view(self):
        """Tests user verification.

        Request validation link to verify the user account.
        """
        # Just ensuring that the user has not been verified yet.
        self.assertFalse(self.user.is_verified)

        link = self.user.get_validation_link(absolute=False)
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['user'], User)
        self.assertEqual(self.user, response.context['user'])
        self.assertIsInstance(response.context['executed'], bool)
        # The "executed" variable is a flag to control interface when the
        # verification action is executed.
        self.assertTrue(response.context['executed'])
        # Ensuring that the action has been updated the user record.
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_user_already_verified(self):
        """Test request to validation link when the user is already verified.

        When a user is already verified then the view will do nothing. Just
        the interface will show an warn informing that the user already is
        an active user.
        """
        # Make sure user is already verified.
        self.user.is_verified = True
        self.user.save()

        # Get a validation link and request it to try validate the account.
        link = self.user.get_validation_link(absolute=False)
        response = self.client.get(link)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['user'], User)
        self.assertEqual(self.user, response.context['user'])
        self.assertIsInstance(response.context['executed'], bool)

        # The variable executed must be False because no action was executed.
        self.assertFalse(response.context['executed'])

    def test_try_arbitrary_uidb64(self):
        """Use an arbitrary parameter [uidb64] when request validation link.

        The uidb64 param is the user id encoded in base64, so it identify
        the user that will be verified. Of course it is not allowed to use an
        arbitrary parameter.
        """
        link = self.user.get_validation_link()


@tag('integration')
class TestRenewValidationLinkView(TestCase):
    """Test cases of the Renew Validation Link View."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.client = Client()
        self.user = mommy.make(User)
        self.user_pass = self.user.password
        self.user.set_password(self.user_pass)
        self.user.save()

    def test_renew_validation_link_view(self):
        """Tests the renew validation link view."""
        endpoint = reverse('account:renew_validation_link')
        logged = self.client.login(username=self.user.username,
                                    password=self.user_pass)
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
