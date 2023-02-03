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

<<<<<<< HEAD
# Project modules
=======
# First party
from abstracts.utils import get_eta_time

# Local
>>>>>>> e664215b0d4663ee403b3fff2b41fcf64a55abe4
from .models import Player
from .tasks import (
    notify,
)


mail_addresses = [
    # 'kobit53104@webonoid.com',
    'ksmakov@gmail.com'
]


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
<<<<<<< HEAD
    """
        Сигнал, срабатывающий при сохранении Игрока,
        при выполнении отправляет сообщение на почту
    """
    if not created:
        return

    send_mail(
        subject='Новый свободный агент',
        message='Доступен новый игрок на трансферном рынке',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=mail_addresses,
        fail_silently=False
    )
=======
    """Post-save Player."""
    if created:
        notify.apply_async(
            args=('Created', instance.fullname, str(instance)),
            eta=get_eta_time(10)
        )

        return

    if instance.status == Player.STATUS_FREE_AGENT:
        notify.apply_async(
            args=('FreeAgent', instance.fullname, str(instance)),
            eta=get_eta_time(10)
        )
        return

    if instance.status == Player.STATUS_RETIRED:
        notify.apply_async(
            args=('Retired', instance.fullname, str(instance)),
            eta=get_eta_time(10)
        )
        return

>>>>>>> e664215b0d4663ee403b3fff2b41fcf64a55abe4


@receiver(
    post_delete,
    sender=Player
)
def post_delete_player(
    sender: ModelBase,
    instance: Player,
    **kwargs: Any
) -> None:
<<<<<<< HEAD
    """
        Сигнал, срабатывающий при удалении Игрока.
        При выполнении отправляет сообщение на почту
    """
    send_mail(
        subject='Игрок завершил карьеру',
        message=(
            f'Игрок {instance.surname} {instance.name} завершил карьеру\n'
            f'команда игрока {instance.team.title}'
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=mail_addresses,
        fail_silently=False
    )
=======
    """Post-delete Player."""
    pass
>>>>>>> e664215b0d4663ee403b3fff2b41fcf64a55abe4
