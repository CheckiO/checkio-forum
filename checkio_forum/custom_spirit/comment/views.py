# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404

from spirit.core.utils import json_response
from checkio_forum.custom_spirit.comment.forms import CommentImageForm


@require_POST
@login_required
def image_upload_ajax(request):
    if not request.is_ajax():
        return Http404()

    form = CommentImageForm(user=request.user, data=request.POST, files=request.FILES)

    if form.is_valid():
        image_url = form.save()
        return json_response({'url': image_url, })

    return json_response({'error': dict(form.errors.items()), })
