# Python
from typing import Any

# Django
from django.conf import settings
from django.core.mail import send_mail

# First party
from settings.celery import app

# Local
from main.models import Player


@app.task
def send_report_for_new_players(*args: Any):
    data: list = []
    for player in Player.objects.filter(status=Player.STATUS_FREE_AGENT):
        data.append(
            f'{player.name} {player.surname}, возраст: {player.age}, сила: {player.power}'
        )
    
    send_mail(
        f': Отчет по новым игрокам',
        "\n".join(data),
        settings.EMAIL_HOST_USER,
        [args[0]],
        fail_silently=False
    )

    print('CALLED: send_report_for_new_player')





