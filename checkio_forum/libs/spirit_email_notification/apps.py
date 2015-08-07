from django.apps import AppConfig


class EmailNotificationConfig(AppConfig):
    name = 'checkio_forum.libs.spirit_email_notification'

    def ready(self):
        import checkio_forum.libs.spirit_email_notification.signals  # noqa
