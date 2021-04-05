"""Module with the forms used by the Account application."""
from django import forms
from django.utils.translation import pgettext_lazy, gettext_lazy as _
from django.contrib.auth import password_validation
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.forms import (
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm
)

from .models import User
from .validators import UsernameValidator, RepetitiveValidator, UsernameBlacklistValidator


class PasswordResetForm(BasePasswordResetForm):
    """Form used to request a link to reset the password."""
    email = forms.EmailField(label=_("Email"), max_length=254,
        widget=forms.TextInput(
            attrs={
                'placeholder': pgettext_lazy('Password reset', 'Your email'),
                'type': 'email'
            }
        )
    )

class SetPasswordForm(BaseSetPasswordForm):
    """Form used to set a password."""

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': pgettext_lazy('Password reset', 'New password')
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html()
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': pgettext_lazy('Password reset',
                                             'New password confirmation')
            }
        )
    )

class SignupForm(forms.Form):
    """Form used for signing up the users."""

    username = forms.CharField(label=_('Username'),
        validators=[
            UsernameValidator(),
            MaxLengthValidator(40, message=_('The username is too long.')),
            MinLengthValidator(3, message=_('The username is too short.')),
            RepetitiveValidator(message=_('The username has too many repeating characters.')),
            UsernameBlacklistValidator()
        ],
        max_length=40,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'placeholder': pgettext_lazy('Sign Up Page', 'Username')
            }
        )
    )
    email = forms.EmailField(label=_('Email'),
        validators=[
            MaxLengthValidator(254, message=_('The email is too long.')),
        ],
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'placeholder': pgettext_lazy('Sign Up Page', 'Email'),
                'type': 'email'
            }
        )
    )
    password1 = forms.CharField(label=_('Password'),
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': pgettext_lazy('Sign Up Page', 'Password')
            }
        )
    )
    password2 = forms.CharField(label=_('Password confirmation'),
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': pgettext_lazy('Sign Up Page',
                                             'Password confirmation')
            }
        )
    )

    def clean(self):
        """Validates the form fields."""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')

        if pass1 != pass2:
            error_msg = _('Password and Confirm Password does not match.')
            self.add_error('password2', error_msg)

        # Check if username is unique. Case-insensitive.
        if User.all_objects.filter(username__iexact=username).exists():
            error_msg = _('This username is already associated with '\
                'an account on our website.')
            self.add_error('username', error_msg)

        # Validate Password.
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password2', error)
