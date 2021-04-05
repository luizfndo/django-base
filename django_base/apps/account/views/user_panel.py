"""Module with view classes used in the user panel page."""
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class UserPanelView(LoginRequiredMixin, View):
    """The User Panel view class."""

    def get(self, request):
        """Handle the HTTP GET requests."""
        return render(request, 'account/user-panel.html')
