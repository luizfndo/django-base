"""URL routes of the account application."""
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

from django_base.apps.account.views.user_panel import UserPanelView
from django_base.apps.account.views.account import (
    SignupView,
    SignupDoneView,
    SignupValidationView,
    RenewValidationLinkView,
    AccountDeleteView,
    AccountRecoveryView
)

from .forms import PasswordResetForm, SetPasswordForm



app_name = 'account'


urlpatterns = [
    path(_('user/'), UserPanelView.as_view(), name='user-panel'),
    path(_('sign-up/'), SignupView.as_view(), name='signup'),
    path(_('sign-up/done/'), SignupDoneView.as_view(), name='sign-up-done'),

    # Login page.
    path(_('login/'), auth_views.LoginView.as_view(
        template_name='account/login.html',
        redirect_authenticated_user=True,
        authentication_form=AuthenticationForm
    ), name='login'),

    # Logout page.
    path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),

    # Put an e-mail to send a link with the url to reset the password.
    path(_('password-reset/'), auth_views.PasswordResetView.as_view(
        template_name='account/password_reset_form.html',
        success_url=reverse_lazy('account:password_reset_done'),
        email_template_name='account/password_reset_email.html',
        form_class=PasswordResetForm
    ), name='password_reset'),

    # Page showed after emailed with the link to reset the passwork.
    path(_('password-reset/done/'), auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ), name='password_reset_done'),

    # After click on the link will go to this endpoint.
    path(_('reset/<uidb64>/<token>/'), auth_views.PasswordResetConfirmView\
         .as_view(
            template_name='account/password_reset_confirm.html',
            form_class=SetPasswordForm,
            success_url=reverse_lazy('account:password_reset_complete')
         ),
         name='password_reset_confirm'),

    # This page will be shown after password has been changed.
    path(_('reset/done/'), auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Form to change the password.
    path(_('password-change/'), auth_views.PasswordChangeView.as_view(
        template_name='account/password_change_form.html'
    ), name='password_change'),

    # Page shown after the password has been changed.
    path(_('password-change/done/'), auth_views.PasswordChangeView.as_view(
        template_name='account/password_change_done.html'
    ), name='password_change_done'),

    # E-mail validation.
    path(_('validation/<uidb64>/<token>/'), SignupValidationView.as_view(),
         name='validation'),

    path(_('renew-validation-link/'), RenewValidationLinkView.as_view(),
         name='renew_validation_link'),

    # Account delete.
    path(_('delete/'), AccountDeleteView.as_view(), name='delete'),

    # Account recovery
    path(_('recovery/<uidb64>/<token>/'), AccountRecoveryView.as_view(),
         name='recovery'),
]
