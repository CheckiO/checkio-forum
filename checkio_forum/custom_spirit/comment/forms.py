# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _

from checkio_forum.libs.storages.s3 import MediaStorageS3
from storages.backends.sftpstorage import SFTPStorage


from spirit.core import utils


class CommentImageForm(forms.Form):

    image = forms.ImageField()

    def __init__(self, user=None, *args, **kwargs):
        super(CommentImageForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_image(self):
        file = self.cleaned_data['image']

        if file.image.format.lower() not in settings.ST_ALLOWED_UPLOAD_IMAGE_FORMAT:
            raise forms.ValidationError(
                _("Unsupported file format. Supported formats are %s."
                  % ", ".join(settings.ST_ALLOWED_UPLOAD_IMAGE_FORMAT))
            )

        return file

    def save(self):
        file = self.cleaned_data['image']
        file_hash = utils.get_hash(file)
        file.name = ''.join((file_hash, '.', file.image.format.lower()))
        save_to_file = settings.COMMENT_FILES_FOLDER + '/' + file.name
        default_storage.save(save_to_file, file)
        return default_storage.url(save_to_file)
