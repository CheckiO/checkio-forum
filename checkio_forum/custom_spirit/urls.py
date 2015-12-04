# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url

import checkio_forum.custom_spirit.comment.urls


urlpatterns = [
    url(r'^comment/', include(checkio_forum.custom_spirit.comment.urls, namespace='comment')),
]


# urlpatterns = [
#     url(r'^', include(patterns, namespace='custom_spirit', app_name='custom_spirit')),
# ]
