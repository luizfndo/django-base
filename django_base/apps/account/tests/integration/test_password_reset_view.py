"""Module with test cases of the Password Reset View."""
from model_mommy import mommy
from django.core import mail
from django.urls import reverse
from django.test import TestCase, Client, tag

from django_base.apps.account.models import User


@tag('integration')
class TestPasswordResetView(TestCase):
    """Test cases of the Password Reset View."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.client = Client()

    def test_endpoint(self):
        """Tests whether Password Reset endpoint exists."""
        endpoint = reverse('account:password_reset')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)

    def test_validation_required_fields(self):
        """Test the validation of required fields."""
        data = {}
        endpoint = reverse('account:password_reset')
        response = self.client.post(endpoint, data)
        self.assertFormError(response, 'form', 'email',
            'This field is required.')

    def test_email_nonexistent_user(self):
        """Test submit an email to request a link to password reset."""
        data = {'email': 'abc@gmail.com'}

        endpoint = reverse('account:password_reset')
        done_page = reverse('account:password_reset_done')
        response = self.client.post(endpoint, data)

        # Email with password reset link should not be sent.
        self.assertEqual(len(mail.outbox), 0)

        self.assertRedirects(response, done_page)

    def test_email_valid_user(self):
        """Test submit an email to request a link to password reset."""
        user = mommy.make(User)
        user_pass = user.password
        user.set_password(user_pass)
        user.save()

        mail.outbox = []

        data = {'email': user.email}

        endpoint = reverse('account:password_reset')
        done_page = reverse('account:password_reset_done')
        response = self.client.post(endpoint, data)

        # Email with password reset link.
        self.assertEqual(len(mail.outbox), 1)

        self.assertRedirects(response, done_page)
