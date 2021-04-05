"""Module with view classes used in the account system."""
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from ..models import User
from ..forms import SignupForm
from ..tokens import ValidationTokenGenerator


INTERNAL_RECOVERY_URL_TOKEN = '_account_recovery_token'


class SignupView(View):
    """The Sign Up view class."""

    def get(self, request):
        """Handle the HTTP GET requests."""
        form = SignupForm()
        return render(request, 'account/signup.html', {'form': form})

    def post(self, request):
        """Handle the HTTP POST requests."""
        form = SignupForm(request.POST)
        if form.is_valid():
            # Trim white spaces from edges and force lowercase.
            user_name = form.cleaned_data['username'].strip().lower()

            user_email = form.cleaned_data['email']
            user_pass = form.cleaned_data['password1']
            User.objects.create_user(user_name, user_email, user_pass)
            user = authenticate(request, username=user_name,
                                password=user_pass)
            if user is not None:
                login(request, user)
                return redirect('account:sign-up-done')
            else:
                pass
        return render(request, 'account/signup.html', {'form': form})


class SignupDoneView(View):
    """The Sign Up Done view class."""

    def get(self, request):
        """Handle the HTTP GET requests."""
        if request.user.is_authenticated and not request.user.is_verified:
            return render(request, 'account/signup_done.html')
        return redirect('home')


class SignupValidationView(View):
    """The Sign Up Validation view class."""

    def get(self, request, uidb64, token):
        """Handle the HTTP GET requests."""
        executed = False
        user = self._get_user(uidb64)
        if user:
            token_gen = ValidationTokenGenerator()
            valid = token_gen.check_token(user, token)
            if valid and not user.is_verified:
                user.is_verified = True
                user.save()
                executed = True
        return render(request, 'account/validation.html', {
            'user': user,
            'executed': executed
        })

    # pylint: disable=no-self-use
    def _get_user(self, uidb64):
        """Returns the user object from the the uidb64 parameter."""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user


class RenewValidationLinkView(LoginRequiredMixin, View):
    """The Renew Validation Link view class."""

    def get(self, request):
        """Handle the HTTP GET requests."""
        request.user.send_validation_link()
        return render(request, 'account/renew_validation_link.html')


class AccountDeleteView(LoginRequiredMixin, View):
    """The Account Delete view class.

    The Account Delete action is run through a POST request, because of possible
    attacks like spam with a false link.
    """

    redirect_field_name = None # Does not redirect back after login.

    def post(self, request):
        """Handle the HTTP POST requests."""
        link_recovery = request.user.get_recovery_link(absolute=False)
        request.user.send_recovery_link()

        # Delete (Logical exclusion) and logout the user.
        request.user.delete()
        logout(request)

        return render(request, 'account/account_delete_done.html', {
            'link_recovery': link_recovery
        })


class AccountRecoveryView(View):
    """The Account Recovery view class."""

    token_generator = ValidationTokenGenerator()

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        """Dispatch HTTP requests."""
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RECOVERY_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RECOVERY_URL_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RECOVERY_URL_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RECOVERY_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)
        return HttpResponseNotFound(_('The user could not be found.'))

    def get_user(self, uidb64):
        """Returns the user object from the the uidb64 parameter."""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.all_objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get(self, request, uidb64, token):
        """Handle the HTTP GET requests."""
        if self.user and self.validlink:
            self.user.deleted = None
            self.user.save()
            return render(request, 'account/recovery-done.html', {
                'user': self.user
            })
        return HttpResponseNotFound(_('The user could not be found.'))


class UsernameCheckView(View):
    """The Username Check view class."""

    def get(self, request):
        """Handle the HTTP GET requests."""
        valid = False
        username = request.GET.get('username')
        if username:
            # Trim white spaces from edges and force lowercase.
            username = username.strip().lower()
            user = User.objects.filter(username=username).exists()
            if not user:
                # forbidden = UsernameBlacklist.objects.filter(username=username)\
                #     .exists()
                # if not forbidden:
                #     valid = True
                valid = True

        return JsonResponse(valid, safe=False)
