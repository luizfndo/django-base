"""Module with test cases of the Login view."""
from model_mommy import mommy
from django.conf import settings
from django.urls import reverse
from django.test import TestCase, Client, tag

from django_base.apps.account.models import User


@tag('integration')
class TestLoginView(TestCase):
    """Test cases of the Login view."""

    def setUp(self):
        """Set up the client (dummy browser) and useful attributes."""
        self.client = Client()

    def test_endpoint(self):
        """Tests whether login endpoint exists."""
        endpoint = reverse('account:login')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)

    def test_validate_required_fields(self):
        """Test the validation of required fields."""
        endpoint = reverse('account:login')
        response = self.client.post(endpoint, {})
        self.assertFormError(response, 'form', 'username',
            'This field is required.')
        self.assertFormError(response, 'form', 'password',
            'This field is required.')

    def test_invalid_login(self):
        """Tests submission of invalid data to login view."""
        endpoint = reverse('account:login')
        data = {'username': 'user123', 'password': 'mypassword123'}
        response = self.client.post(endpoint, data)

        msg = 'Please enter a correct username and password.'
        self.assertRegex(response.context['form'].errors['__all__'][0], msg)

    def test_valid_login(self):
        """Tests submission of valid data to login view."""
        user = mommy.make(User)
        user_pass = user.password
        user.set_password(user_pass)
        user.save()

        endpoint = reverse('account:login')
        data = {'username': user.username, 'password': user_pass}
        response = self.client.post(endpoint, data)

        # The target_status_code is 302 because of the language redirect.
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL,
                             target_status_code=302)

    def test_next_parameter(self):
        """Tests the next parameter.

        The next parameter in the querystring should cause a redirect
        to its value when login successfully.
        """
        user = mommy.make(User)
        user_pass = user.password
        user.set_password(user_pass)
        user.save()

        my_account = reverse('account:user-panel')
        endpoint = reverse('account:login')
        data = {'username': user.username, 'password': user_pass}
        response = self.client.post(f'{endpoint}?next={my_account}', data)
        self.assertRedirects(response, my_account)
