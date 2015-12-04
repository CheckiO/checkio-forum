# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, patterns

from checkio_forum.custom_spirit.comment import views

urlpatterns = [
    url(r'^upload/$', views.image_upload_ajax, name='image-upload-ajax'),
]
