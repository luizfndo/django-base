"""Module with the URL routers."""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('admin/', admin.site.urls),
    path(_('account/'), include('django_base.apps.account.urls', namespace='account')),
    path('thumbnail/', include('django_base.apps.thumbnail.urls', namespace='thumbnail')),
    path('', include('django_base.apps.website.urls', namespace='website')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)