from django.apps import AppConfig


class FilesConfig(AppConfig):
    name = 'files'

    def ready(self):
        from .services import init_storage
        init_storage()
