from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notification"

    def ready(self):
        from watson import search as watson
        Notification = self.get_model('Notification')
        watson.register(Notification, fields=('verb',))