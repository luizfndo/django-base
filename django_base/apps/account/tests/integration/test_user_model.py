"""This module has the integration tests of the user model."""
import re
import os
from model_mommy import mommy

from django.core import mail
from django.core.validators import URLValidator
from django.utils.http import urlsafe_base64_decode
from django.db.utils import IntegrityError
from django.test import TestCase

from django_base.apps.account.models import User
from django_base.apps.account.tokens import ValidationTokenGenerator


class TestUserModel(TestCase):
    """User model test cases."""

    def test_user_create(self):
        """Test the default attributes of a new user."""
        user = mommy.make(User)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)

    def test_username_normalization(self):
        """Tests the username normalization.

        The save method will turn the username in lowercase.
        """
        user = mommy.make(User, username='MYUSER')
        self.assertEqual(user.username, 'myuser')

    def test_user_logic_exclusion(self):
        """Test the logic exclusion of users."""
        user1 = mommy.make(User)
        user1.delete()

        # Should retrieve nothing.
        users = User.objects.all()
        self.assertEqual(len(users), 0)

        # Should retrieve nothing again.
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username=user1.username)

    def test_unique_username_constraint(self):
        """Tests unique username constraint."""
        user1 = mommy.make(User)
        with self.assertRaises(IntegrityError):
            user2 = mommy.make(User, username=user1.username)

    def test_get_full_name(self):
        """Tests the display name function.

        The function should return the value of the display name field when
        there is one. Otherwise should return the value of the username field.
        """
        user = mommy.make(User)
        self.assertEqual(user.get_display_name, user.username)

        user.display_name = 'My Display Name'
        user.save()

        self.assertEqual(user.get_display_name, user.display_name)


    def test_get_full_name(self):
        """Test the method used to get the full name of the user.

        The full name should be composed of the first name and the last name.
        """
        user = mommy.make(User, first_name='Ashley', last_name='Aires')
        full_name = f'{user.first_name} {user.last_name}'
        self.assertIsInstance(user.get_full_name(), str)
        self.assertEqual(user.get_full_name(), full_name)

    def test_get_short_name(self):
        """Test the method used to get the short name f the user.

        The short name should be the first name of the user.
        """
        user = mommy.make(User)
        self.assertIsInstance(user.get_short_name(), str)
        self.assertEqual(user.get_short_name(), user.first_name)

    def test_email_user(self):
        """Test the method used to email the user.

        The method should send an email to the user.
        """
        user = mommy.make(User)
        subject = 'Subject of the email.'
        message = 'Message of the email.'
        mail.outbox = []  # Ensure the mailbox empty.
        user.email_user(subject, message)
        self.assertIn(user.email, mail.outbox[0].to)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].body, message)

    def test_get_validation_token(self):
        """Test the method used to get the validation token.

        The validation token is composed by the user id and a salt key.
        Usually this token is sent to the user by email and after the user
        click on the link with the token, so the account is validated.
        """
        user = mommy.make(User)
        token = user._get_validation_token()
        self.assertIsInstance(token, str)

        token_gen = ValidationTokenGenerator()
        self.assertTrue(token_gen.check_token(user, token))

    def test_get_id_base64(self):
        """Test the method used to return the id encoded in base64.

        The method should return a bytestring containing the user id encoded
        in base64.
        """
        user = mommy.make(User)
        uidb64 = user._get_id_base64()
        self.assertIsInstance(uidb64, bytes)
        self.assertEqual(user.pk, int(urlsafe_base64_decode(uidb64).decode()))

    def test_get_id_base64_user_pk_none(self):
        """Test the method used to return the id enconded in base64.

        The method should raise an exception ValueError when the user does not
        have an associate id yet.
        """
        user = User()
        with self.assertRaises(ValueError):
            user._get_id_base64()

    def test_get_validation_link_absolute(self):
        """Test the method used to return a validation link.

        The method should return the link that will be used to validate the
        user's account. The method should allow to return either an absolute
        link or a relative link. This test will cover the return of an
        absolute link.
        """
        user = mommy.make(User)
        link = user.get_validation_link()
        self.assertIsInstance(link, str)
        self.assertIsNone(URLValidator()(link))

    def test_get_validation_link_relative(self):
        """Test the method used to return a validation link.

        The method should return the link that will be used to validate the
        user's account. The method should allow to return either an absolute
        link or a relative link. This test will cover the return of a relative
        link.
        """
        user = mommy.make(User)
        path = user.get_validation_link(absolute=False)
        self.assertTrue(os.path.isabs(path))

    def test_send_validation_link(self):
        # ToDo: Test the send of the validate link to the user.
        pass
