"""Module with tests of the sign up view."""
from django.test import TestCase, Client, tag
from django.urls import reverse


@tag('integration')
class TestSignupView(TestCase):
    """Test cases of the Sign Up view."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.client = Client()

    def test_register_user(self):
        """Tests the user register.

        After sign up successfully the user should be redirect to the Sign Up
        Done page.
        """
        data = {
            'username': 'sdsfsdf',
            'email': 'sdsfsdf@example.com',
            'password1': 'HFDSD334#ds!',
            'password2': 'HFDSD334#ds!'
        }
        done = reverse('account:sign-up-done')
        endpoint = reverse('account:signup')
        response = self.client.post(endpoint, data)
        self.assertRedirects(response, done)

    def test_form_validation(self):
        """Tests the user form validation."""
        data = {}
        endpoint = reverse('account:signup')
        response = self.client.post(endpoint, data)
        self.assertFormError(response, 'form', 'username',
            'This field is required.')
        self.assertFormError(response, 'form', 'email',
            'This field is required.')
        self.assertFormError(response, 'form', 'password1',
            'This field is required.')
        self.assertFormError(response, 'form', 'password2',
            'This field is required.')
