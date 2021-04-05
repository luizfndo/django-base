"""Module with tests of the User Form."""
from model_mommy import mommy
from django.test import TestCase, tag
from django.utils.translation import gettext_lazy as _

from django_base.apps.account.forms import SignupForm
from django_base.apps.account.models import User


@tag('integration')
class TestSignupForm(TestCase):
    """Test cases of the User Form."""

    def test_email_validation(self):
        """Tests the email validation."""
        data = {
            'username': 'asdasd',
            'email': 'invalid@email',
            'password1': '123',
            'password2': '123'
        }

        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email'))
        self.assertIn(_('Enter a valid email address.'), form.errors['email'])

    def test_confirm_password(self):
        """Tests the password confirmation."""
        data = {
            'username': 'asdasd',
            'email': 'contact@provider.com',
            'password1': '123',
            'password2': '321'
        }

        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

        error_msg = _('Password and Confirm Password does not match.')
        self.assertIn(error_msg, form.errors['password2'])

    def test_required_fields(self):
        """Tests the required fields of the form."""
        required_msg = _('This field is required.')
        data = {'username':'', 'email': '','password1': '','password2': ''}
        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(required_msg, form.errors['username'])
        self.assertIn(required_msg, form.errors['email'])
        self.assertIn(required_msg, form.errors['password1'])
        self.assertIn(required_msg, form.errors['password2'])

    def test_validation_username_unique(self):
        """Tests the username validation.

        The username must be unique, even though the system is based on logical
        exclusion. The username is case-insensitive.
        """
        username = 'my_username'

        user1 = mommy.prepare(User, username=username)
        user1.set_password(user1.password)
        user1.full_clean()
        user1.save()

        user2 = mommy.prepare(User, username=username)

        data = {
            'username': user2.username,
            'email': user2.email,
            'password1': user2.password,
            'password2': user2.password
        }

        form = SignupForm(data)
        self.assertFalse(form.is_valid())

        error_msg = _('This username is already associated with '\
            'an account on our website.')
        self.assertIn(error_msg, form.errors['username'])

    def test_signup_form(self):
        """Tests the submission of valid data."""
        data = {
            'username': 'abcd',
            'email': 'talktous@gmail.com',
            'password1': 'SDS#!#sdfsd',
            'password2': 'SDS#!#sdfsd'
        }
        form = SignupForm(data)
        self.assertTrue(form.is_valid())
