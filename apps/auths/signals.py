# Python
from typing import Any

# Django
# from django.conf import settings
# from django.core.mail import send_mail
from django.db.models.base import ModelBase
from django.db.models.signals import (
    post_save
)
from django.dispatch import receiver

# First party
# from abstracts.utils import get_eta_time

# Local
from .models import Client
# from .tasks import (
#     send_report_for_new_players,
# )


@receiver(
    post_save,
    sender=Client
)
def post_save_client(
    sender: ModelBase,
    instance: Client,
    created: bool,
    **kwargs: Any
) -> None:
    """Post-save Client."""
    pass
    # if created:
    #     send_report_for_new_players.apply_async(
    #         args=(instance.email, ),
    #         eta=get_eta_time(days=30)
    #     )
