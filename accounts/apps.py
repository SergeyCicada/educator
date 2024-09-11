from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Class for signals account
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Аккаунты'

    def ready(self):
        import accounts.signals
