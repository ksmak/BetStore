# Python
from typing import Any

# Django
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.base import ModelBase
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Local
from .models import Player


@receiver(
    post_save,
    sender=Player
)
def post_save_player(
    sender: ModelBase,
    instance: Player,
    created: bool,
    *args: Any,
    **kwargs: Any
) -> None:
    """Post-save Player."""
    if not created:
        return

    send_mail(
        'Новый свободный агент',
        'Доступен новый игрок на трансферном рынке',
        settings.EMAIL_HOST_USER,
        [
            'kobit53104@webonoid.com',
            'ksmakov@gmail.com'
        ],
        fail_silently=False
    )

@receiver(
    pre_delete,
    sender=Player
)
def post_delete_player(
    sender: ModelBase,
    instance: Player,
    *args: Any,
    **kwargs: Any
) -> None:
    """Post-delete Player."""
    send_mail(
        'Игрок завершил карьеру',
        f'Игрок {instance.surname} {instance.name} завершил карьеру\nкоманда игрока {instance.team.title}',
        settings.EMAIL_HOST_USER,
        [
            'kobit53104@webonoid.com',
            'ksmakov@gmail.com'
        ],
        fail_silently=False
    )