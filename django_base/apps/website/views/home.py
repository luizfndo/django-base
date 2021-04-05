""""Module with the Homepage view class."""
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control


class HomeView(View):
    """View of the Homepage."""

    @method_decorator(cache_control(public=True, max_age=86400,
                                    s_maxage=2592000))
    def get(self, request):
        """Handle the HTTP GET method."""

        return render(request, 'website/home.html')
