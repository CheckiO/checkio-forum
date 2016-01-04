from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from spirit.comment.models import Comment
from spirit.topic.notification.models import TopicNotification


@receiver(post_save, sender=Comment)
def send_notifications(instance, **kwargs):
    topic = instance.topic
    notifications = TopicNotification.objects.filter(
        topic=topic,
        is_active=True
    ).exclude(
        user=instance.user
    )
    quote_url = reverse(
        'spirit:comment:publish',
        kwargs={'topic_id': topic.id, 'pk': instance.id}
    )

    body_context = {
        'comment': instance,
        'quote_url': quote_url,
        'domain': settings.DOMAIN
    }
    received_emails = set()
    body = render_to_string('spirit_email_notification/new_comment.html', body_context)
    for notification in notifications:
        send_mail(
            u'EoC Comment. {}'.format(topic.title),
            body,
            settings.DEFAULT_FROM_EMAIL,
            [notification.user.email])
        received_emails.add(notification.user.email)

    from spirit.core.utils.markdown import Markdown

    md = Markdown()
    md.render(instance.comment)
    mentions = md.get_mentions()

    if mentions:
        body_mentioning = render_to_string('spirit_email_notification/mention.html', body_context)
        for user in mentions.values():
            if instance.user == user:
                continue
            if user.email in received_emails:
                continue
            send_mail(
                u'EoC Mention. {}'.format(topic.title),
                body_mentioning,
                settings.DEFAULT_FROM_EMAIL,
                [user.email])
            received_emails.add(user.email)
