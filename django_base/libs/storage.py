"""Module with the storage classes."""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Storage manager of static files."""

    bucket_name = settings.STATIC_AWS_BUCKET
    custom_domain = settings.STATIC_CUSTOM_DOMAIN


class MediaStorage(S3Boto3Storage):
    """Storage manager of uploaded files."""

    bucket_name = settings.MEDIA_AWS_BUCKET
    custom_domain = settings.MEDIA_CUSTOM_DOMAIN
