from spirit.comment.models import Comment
from spirit.topic.models import Topic

from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'comment',)
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'comment')

admin.site.register(Comment, CommentAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'title',)
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'title')

admin.site.register(Topic, TopicAdmin)
