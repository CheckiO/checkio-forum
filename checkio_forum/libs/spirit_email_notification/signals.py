from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from spirit.comment.models import Comment
from spirit.topic.notification.models import TopicNotification
# TODO:

@receiver(post_save, sender = TopicNotification)
def send_email_notification(sender, instance, raw, **kwargs):
    if raw:
        return
    Topic_not = TopicNotification.objects.all()
    for topic in Topic_not:
        if topic.is_read == False:
            quote_url = 'sdfsdf'
            body_context = {
                'comment': topic.comment,
                'quote_url': quote_url,
                'domain': settings.DOMAIN
            }
            body = render_to_string('spirit_email_notification/new_comment.html', body_context)
            send_mail('EoC Comment. {}'.format(topic.comment.topic.title),
                body, settings.DEFAULT_FROM_EMAIL,
                [topic.user.email])


# TODO:


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
