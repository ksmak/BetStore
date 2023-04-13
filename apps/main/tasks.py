# Python
from typing import Any
import random
# Django
# from django.conf import settings
from django.core.exceptions import ValidationError
# from django.core.mail import send_mail

# First party
from settings.celery import app

# Local
from .models import (
    Player,
    Event,
    Team
)

from abstracts.connectors import (
    BaseConnector,
    RedisConnector,
    FileConnector,
)


@app.task(
    name='change_player_age'
)
def change_player_age(*args: Any) -> None:
    for player in Player.objects.all():
        current_age: int = player.age
        player.age = current_age + 1
        try:
            player.save(update_fields=('age',))
            print(f'Player: {player.id} success')
        except ValidationError:
            print(f'Player: {player.id} failed')

    print('CALLED: CHANGE PLAYER AGE')


@app.task
def notify(*args: Any) -> None:
    # if args[0] == 'Created':
    #     send_mail(
    #         f'Новый игрок: {args[1]}',
    #         f'Доступен новый игрок на трансферном рынке: {args[2]}',
    #         settings.EMAIL_HOST_USER,
    #         [settings.EMAIL_SEND_ADDR],
    #         fail_silently=False
    #     )
    # elif args[0] == 'FreeAgent':
    #     send_mail(
    #         f'Свободный агент: {args[1]}',
    #         f'Доступен игрок на трансферном рынке: {args[2]}',
    #         settings.EMAIL_HOST_USER,
    #         [settings.EMAIL_SEND_ADDR],
    #         fail_silently=False
    #     )
    # elif args[0] == 'Retired':
    #     send_mail(
    #         f'Завершил карьеру: {args[1]}',
    #         f'Игрок завершил карьеру: {args[2]}',
    #         settings.EMAIL_HOST_USER,
    #         [settings.EMAIL_SEND_ADDR],
    #         fail_silently=False
    #     )
    print('CALLED: NOTIFY')


def get_two_teams() -> list[Team, Team]:
    teams = Team.objects.all()
    team_1 = teams[random.randrange(0, len(teams))]
    team_2 = teams[random.randrange(0, len(teams))]
    while team_1 == team_2:
        team_1 = teams[random.randrange(0, len(teams))]
        team_2 = teams[random.randrange(0, len(teams))]

    return [team_1, team_2]


@app.task
def create_event(**kwargs: Any) -> None:
    team_1, team_2 = get_two_teams()

    Event.objects.create(
        status=Event.STATUS_FUTURE,
        team_1=team_1,
        team_2=team_2
    )

    print(f'CALLED: Create event {team_1} {team_2}')


@app.task
def delete_cache(key: str, connector: str) -> None:
    r_connector: BaseConnector
    if connector == 'redis':
        r_connector = RedisConnector()
    elif connector == 'file':
        r_connector = FileConnector()
    else:
        raise ValueError('Unknown connector type!')

    r_connector.delete(key)
