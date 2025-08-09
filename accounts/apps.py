from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from watson import search as watson
        User = self.get_model('CustomUser')
        watson.register(User, fields=('verb',))