# Python
import random
from typing import Any

# Third party
import names
import requests
from requests.models import Response

# Django
from django.core.management.base import BaseCommand

# First party
from main.models import (
    Player,
    Stadium,
    Team
)
from abstracts.decorators import performance_counter


class Command(BaseCommand):
    """Custom command for filling up database."""

    help = 'Custom command for filling up database.'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def generate_players(self) -> None:
        PLAYERS_COUNT: int = 250
        MAX_POWER: int = 99
        MIN_POWER: int = 50
        MAX_AGE: int = 40
        MIN_AGE: int = 17

        players_count: int = Player.objects.count()
        state: bool = bool(players_count < PLAYERS_COUNT)
        if not state:
            return

        count_range: int = PLAYERS_COUNT - players_count

        _: int
        for _ in range(count_range):
            Player.objects.create(
                name=names.get_first_name(
                    gender='male'
                ),
                surname=names.get_last_name(),
                power=random.randrange(
                    MIN_POWER,
                    MAX_POWER
                ),
                age=random.randrange(
                    MIN_AGE,
                    MAX_AGE
                )
            )

    def generate_teams_and_stadiums(self) -> None:

        def generate_stadium_title(code: str) -> str:
            if isinstance(code, tuple):

                return 'Some Stadium'

            return f'{code} Stadium'

        countries_url: str = (
            'https://raw.githubusercontent.com/annexare/Countries/master/data/'
            'countries.json'
        )
        clubs_url: str = (
            'https://raw.githubusercontent.com/openfootball/football.json/'
            'master/2020-21/{}.1.clubs.json'
        )
        leagues: tuple[str, ...] = (
            'en',
            'es',
            'it'
        )
        country_objs: dict[str, Any] = requests.get(countries_url).json()
        countries: dict[str, dict[str, Any]] = {}
        _: str
        data: dict[str, Any]
        for _, data in country_objs.items():
            countries[data['name']] = data['capital']

        league: str
        for league in leagues:
            url: str = clubs_url.format(league)

            response: Response = requests.get(url)
            if response.status_code != 200:
                print('Error')
                return

            data: dict[str, str | list[dict[str, str]]] = response.json()
            obj: dict[str, str]
            for obj in data['clubs']:
                capital: str = countries.get(
                    obj['country'],
                    'Unknown'
                )
                stadium: Stadium
                _: bool
                stadium, _ = Stadium.objects.get_or_create(
                    title=generate_stadium_title(
                        obj['code']
                    ),
                    capacity=random.randrange(
                        40000,
                        100000,
                        5000
                    ),
                    city=capital
                )
                Team.objects.get_or_create(
                    title=obj['name'],
                    stadium=stadium
                )

    def sync_data(self) -> None:

        team: Team
        for team in Team.objects.all():
            players: list[Player] = list(
                Player.objects.all()
            )
            random.shuffle(players)
            team.players.set(
                players[:Team.MAX_PLAYERS]
            )

    def update_player_status(self) -> None:

        player: Player
        for player in Player.objects.filter(team__isnull=False):
            player.status = Player.STATUS_TEAM_MEMBER
            player.save(update_fields=('status',))

    def fix_player_min_power(self) -> None:

        # player: Player
        # for player in Player.objects.filter(
        #     power__lt=Player.ADULT_TEAM_MIN_POWER
        # ):
        #     player.power = Player.ADULT_TEAM_MIN_POWER
        #     player.save(update_fields=('power',))

        Player.objects.filter(
            power__lt=Player.ADULT_TEAM_MIN_POWER
        ).update(
            power=Player.ADULT_TEAM_MIN_POWER
        )

    @performance_counter
    def handle(self, *args: Any, **kwargs: Any) -> None:
        """Handles data filling."""
        self.generate_players()
        self.generate_teams_and_stadiums()
        self.sync_data()
        self.update_player_status()
        self.fix_player_min_power()
