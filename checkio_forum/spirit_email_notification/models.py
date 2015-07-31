from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from spirit.models.topic_notification import TopicNotification
from spirit.signals.comment import comment_posted


def send_notification(sender, comment, mentions, **kwargs):
    topic = comment.topic
    notifications = TopicNotification.objects.filter(topic=topic, is_active=True)\
        .exclude(user=comment.user)
    quote_url = reverse('spirit:comment-publish', kwargs={'topic_id': topic.id,
                                                          'pk': comment.id})

    body_context = {
        'comment': comment,
        'quote_url': quote_url,
        'domain': settings.DOMAIN
    }
    done_emails = set()
    body = render_to_string('spirit_email_notification/new_comment.html', body_context)
    for notif in notifications:
        send_mail('EoC Comment. {}'.format(topic.title),
                  body, settings.DEFAULT_FROM_EMAIL,
                  [notif.user.email])
        done_emails.add(notif.user.email)

    body_ment = render_to_string('spirit_email_notification/mention.html', body_context)
    for user in mentions.values():
        if comment.user == user:
            continue
        if user.email in done_emails:
            continue
        send_mail('EoC Mention. {}'.format(topic.title),
                  body_ment, settings.DEFAULT_FROM_EMAIL,
                  [user.email])
        done_emails.add(user.email)


comment_posted.connect(send_notification, dispatch_uid=__name__)
