from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorageS3(S3BotoStorage):
    location = settings.AWS_STATIC_LOCATION


class MediaStorageS3(S3BotoStorage):
    location = settings.AWS_MEDIA_LOCATION
