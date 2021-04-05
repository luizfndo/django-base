"""Module with the integration test cases of the Homepage View."""
from unittest import mock

from django.conf import settings
from django.utils import translation
from django.urls import reverse, resolve
from django.test import TestCase, Client, tag

from django_base.apps.website.views.home import HomeView


# pylint: disable=invalid-name
@tag('integration')
class HomeViewTest(TestCase):
    """Integration test case of the homepage view."""

    def setUp(self):
        """Set up the a dummy web browser (client)."""
        self.client = Client()

    def test_home_page_view_resolves(self):
        """Test the view resolver.

        This test will check if the view returned by the resolve function is
        the correct View.
        """
        endpoint = reverse('home')
        view = resolve(endpoint)
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)

    def test_home_view_get(self):
        """Test the response of a default HTTP GET request."""
        endpoint = reverse('home')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
