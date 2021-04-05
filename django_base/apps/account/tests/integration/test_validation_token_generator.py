"""Module with tests of the Validation Token Generator."""
import hmac
import datetime
from model_mommy import mommy
from django.utils import timezone
from django.test import TestCase, tag

from django_base.apps.account.models import User
from django_base.apps.account.tokens import (
    _today,
    num_elapsed_days,
    make_hash_value,
    ValidationTokenGenerator
)


@tag('integration')
class TestValidationTokenGenerator(TestCase):
    """Test the validation token generator class"""
    token_regex = '[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}'

    def setUp(self):
        """Sets the common objects between the tests."""
        self.generator = ValidationTokenGenerator()
        self.user = mommy.make(User)
        self.user.set_password(self.user.password)
        self.user.save()

    def test_today(self):
        """Test the tokens._today() function of the tokens module."""
        today = _today()
        yesterday = (today - datetime.timedelta(days=1))
        tomorrow  =  (today + datetime.timedelta(days=1))
        self.assertIsInstance(today, datetime.date)
        self.assertGreater(today, yesterday)
        self.assertLess(today, tomorrow)

    def test_num_elapsed_days(self):
        """Test the function tokens.num_elapsed_days(today).

        That function should return the number of days elapsed between
        2001-01-01 until today.
        """
        today = _today()
        elapsed = num_elapsed_days(today)
        self.assertIsInstance(elapsed, int)
        self.assertEqual(elapsed, (today - datetime.date(2001, 1, 1)).days)

    def test_num_elapsed_days_today_parameter_invalid_type(self):
        """Test the function tokens.num_elapsed_days(today).

        The function should raise a TypeError exception when given a parameter
        other than type date.
        """
        today = None
        with self.assertRaisesRegex(TypeError,
                'Invalid type \[{}\] to today parameter.'.format(type(today))):
            elapsed = num_elapsed_days(today)

    def test_make_hash_value(self):
        """Test the function tokens.make_hash_value(user, timestamp).

        The function should return a hash consisting of the user id and the
        timestamp parameter.
        """
        timestamp = num_elapsed_days(_today())
        hash_value = make_hash_value(self.user, timestamp)
        self.assertIsInstance(hash_value, str)
        self.assertEqual(hash_value, f'{self.user.pk}{timestamp}')

    def test_make_hash_value_user_parameter_none(self):
        """Test the function make_hash_value(user, timestamp).

        The function should raise a ValueError exception when given the user
        parameter as None.
        """
        timestamp = num_elapsed_days(_today())
        with self.assertRaisesRegex(ValueError,
                'Invalid value for the user parameter.'):
            hash_value = make_hash_value(None, timestamp)

    def test_make_hash_value_user_pk_none(self):
        """Test the function make_hash_value(user, timestamp).

        The function should raise a ValueError exception when given an user
        parameter without the user id bound.
        """
        user = User()
        timestamp = num_elapsed_days(_today())
        with self.assertRaisesRegex(ValueError,
                'The user id cannot be None.'):
            hash_value = make_hash_value(user, timestamp)

    def test_make_hash_value_timestamp_none(self):
        """Test the function make_hash_value(user, timestamp).

        The function should raise a ValueError exception when given a
        timestamp parameter as None.
        """
        with self.assertRaisesRegex(ValueError,
                'Invalid value for the timestamp parameter.'):
            hash_value = make_hash_value(self.user, None)

    def test_make_token_with_timestamp(self):
        timestamp = num_elapsed_days(_today())
        token = self.generator._make_token_with_timestamp(self.user, timestamp)
        self.assertIsInstance(token, str)
        self.assertRegex(token, self.token_regex)

    def test_make_token(self):
        token = self.generator.make_token(self.user)
        self.assertIsInstance(token, str)
        self.assertRegex(token, self.token_regex)

    def test_check_token(self):
        token = self.generator.make_token(self.user)
        result = self.generator.check_token(self.user, token)
        self.assertIsInstance(result, bool)
        self.assertTrue(result)
