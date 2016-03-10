import os
import re
from StringIO import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage

from spirit.comment.models import Comment

REPLACE_FROM = 'https://empire-forum.s3.amazonaws.com/media/'
REPLACE_TO = 'https://forum.static.empireofcode.com/media/'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        comments = Comment.objects.filter(comment__contains=REPLACE_FROM).order_by('pk')

        for comment in comments:
            comment.comment = comment.comment.replace(REPLACE_FROM, REPLACE_TO)
            comment.comment_html = comment.comment_html.replace(REPLACE_FROM, REPLACE_TO)
            comment.save()
