from django.apps import AppConfig
from django.dispatch import Signal

from .utilities import send_activation_email


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'Блог'


user_registered = Signal(providing_args=['instance'])


def user_registered_dispatcher(sender, **kwargs):
    send_activation_email(kwargs['instance'])


user_registered.connect(user_registered_dispatcher)
