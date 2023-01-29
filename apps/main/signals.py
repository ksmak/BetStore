# Python
from typing import Any

# Django
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.base import ModelBase
from django.db.models.signals import (
    post_delete,
    post_save
)
from django.dispatch import receiver

# First party
from abstracts.utils import get_eta_time

# Local
from .models import Player
from .tasks import (
    notify,
)


@receiver(
    post_save,
    sender=Player
)
def post_save_player(
    sender: ModelBase,
    instance: Player,
    created: bool,
    **kwargs: Any
) -> None:
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


@receiver(
    post_delete,
    sender=Player
)
def post_delete_player(
    sender: ModelBase,
    instance: Player,
    **kwargs: Any
) -> None:
    """Post-delete Player."""
    pass