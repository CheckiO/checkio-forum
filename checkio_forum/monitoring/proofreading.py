from django.conf import settings
from django.core.mail import EmailMessage
from spirit.models.comment import Comment

from django.db.models.signals import post_save


def send_report_email(sender, instance, raw, **kwargs):
    if raw:
        return
    user = instance.user

    if user.username not in settings.MONITORING_PR_USERS:
        return

    subject = u"Proof-Reading comment {}".format(instance.pk)
    body = (u"{text}\n\n"
            u"https://{current_domain}{link}"
            u"").format(text=instance.comment,
                        link=instance.get_absolute_url(),
                        current_domain=settings.DOMAIN)

    EmailMessage(subject, body,
                 settings.DEFAULT_FROM_EMAIL, [settings.MONITORING_PR_READER],
                 headers={'Reply-To': user.email}).send()


post_save.connect(send_report_email, sender=Comment)
