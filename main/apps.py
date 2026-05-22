from django.apps import AppConfig


class MainConfig(AppConfig):
    """Конфигурация приложения EduQuest.

    Django использует этот класс, чтобы подключить приложение к проекту.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'EduQuest'
