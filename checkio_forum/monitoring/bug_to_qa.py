from django.conf import settings
from django.core.mail import send_mail
from spirit.models.comment import Comment

from django.db.models.signals import post_save


def send_report_email(sender, instance, raw, **kwargs):
    if raw:
        return
    topic = instance.topic

    if topic.category.title not in settings.MONITORING_QA_CATEGORIES:
        return

    send_mail(u'EoC QA: ' + topic.title, u'FROM: ' + instance.user.username + u'\n' +
              instance.comment, settings.DEFAULT_FROM_EMAIL + u'\n' +
              u'https://' + settings.DOMAIN + instance.get_absolute_url(),
              settings.MONITORING_QA_RECIPIENTS)

post_save.connect(send_report_email, sender=Comment)
