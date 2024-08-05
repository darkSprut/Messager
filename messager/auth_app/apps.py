from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, pre_delete
from .signals import del_image


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        super().ready()
        pre_delete.connect(del_image, sender='auth_app.Avatar')
