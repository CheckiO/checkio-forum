import os
import re
from StringIO import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage

from spirit.comment.models import Comment


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        media_folder = os.path.join(settings.MEDIA_URL, 'spirit', 'images')
        comments = Comment.objects.filter(comment__contains=media_folder).order_by('pk')

        for comment in comments:
            comment_text = comment.comment
            comment_html = comment.comment_html

            relative_file_urls = re.findall(r'\({}([^(]*)\)'.format(media_folder), comment_text)
            for relative_file_url in relative_file_urls:
                local_file_url = u"{}{}".format(media_folder, relative_file_url)
                full_file_name = u"{}{}".format(settings.BASE_DIR, local_file_url)

                if not os.path.exists(full_file_name):
                    continue

                with open(full_file_name) as fp:
                    raw_file_data = StringIO(fp.read())
                file_name = os.path.basename(full_file_name)
                default_storage.save(file_name, raw_file_data)
                comment_image_url = default_storage.url(file_name)

                comment_text = comment_text.replace(local_file_url, comment_image_url)
                comment_html = comment_html.replace(local_file_url, comment_image_url)

                comment.comment_text = comment_text
                comment.comment_html = comment_html
                comment.save()
