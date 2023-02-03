# Python modules
from typing import Any

# Django modules
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.base import ModelBase
from django.db.models.signals import (
    post_delete,
    post_save
)
from django.dispatch import receiver

# Project modules
from .models import Player
from .tasks import (
    notify,
)


mail_addresses = (
    'bavej31709@fsouda.com',
)


@receiver(
    signal=post_save,
    sender=Player
)
def post_save_player(
    sender: ModelBase,
    instance: Player,
    created: bool,
    **kwargs: Any
) -> None:
    """
        Сигнал, срабатывающий при сохранении Игрока,
        при выполнении отправляет сообщение на почту
    """
    if not created:
        return

    # send_mail(
    #     subject='Новый свободный агент',
    #     message='Доступен новый игрок на трансферном рынке',
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=mail_addresses,
    #     fail_silently=False
    # )


@receiver(
    post_delete,
    sender=Player
)
def post_delete_player(
    sender: ModelBase,
    instance: Player,
    **kwargs: Any
) -> None:
    """
        Сигнал, срабатывающий при удалении Игрока.
        При выполнении отправляет сообщение на почту
    """
    # send_mail(
    #     subject='Игрок завершил карьеру',
    #     message=(
    #         f'Игрок {instance.surname} {instance.name} завершил карьеру\n'
    #         f'команда игрока {instance.team.title}'
    #     ),
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=mail_addresses,
    #     fail_silently=False
    # )
