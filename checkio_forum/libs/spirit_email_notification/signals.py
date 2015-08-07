from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from spirit.comment.models import Comment
from spirit.topic.notification.models import TopicNotification
# from spirit.signals.comment import comment_posted  # TODO:


def send_notification(sender, comment, mentions, **kwargs):
    topic = comment.topic
    notifications = TopicNotification.objects.filter(topic=topic, is_active=True)\
        .exclude(user=comment.user)
    quote_url = reverse('spirit:comment-publish', kwargs={'topic_id': topic.id, 'pk': comment.id})

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

    if mentions:
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

# comment_posted.connect(send_notification, dispatch_uid=__name__)  # TODO:


def send_report_email(sender, instance, raw, **kwargs):
    if raw:
        return
    topic = instance.topic

    if topic.category.title not in settings.MONITORING_QA_CATEGORIES:
        return

    subject = u'EoC QA: {}'.format(topic.title),
    body = u'FROM: {user}\n{text}\nhttps://{current_domain}{link}'.format(
        user=instance.user.username,
        text=instance.comment,
        current_domain=settings.DOMAIN,
        link=instance.get_absolute_url()
    )
    EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.MONITORING_QA_RECIPIENTS
    ).send()

post_save.connect(send_report_email, sender=Comment)


def send_report_email(sender, instance, raw, **kwargs):
    if raw:
        return
    user = instance.user

    if user.username not in settings.MONITORING_PR_USERS:
        return

    subject = u"Proof-Reading comment {}".format(instance.pk)
    body = u"{text}\n\nhttps://{current_domain}{link}".format(
        text=instance.comment, link=instance.get_absolute_url(), current_domain=settings.DOMAIN)

    EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.MONITORING_PR_READER],
        headers={'Reply-To': user.email}
     ).send()

post_save.connect(send_report_email, sender=Comment)
