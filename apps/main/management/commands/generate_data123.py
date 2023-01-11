# Python modules
from typing import Any
import random
import datetime
# Django modules
from django.core.management.base import BaseCommand
from apps.main.models import (
    Player,
    Team,
    Stadium    
)
# Third party modules
import names
import requests
from requests.models import Response

class Command(BaseCommand):
    """Custom command for filling up database"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


    def generate_players(self) -> None:

        PLAYERS_COUNT: int = 250
        MAX_POWER: int = 99
        MIN_POWER: int = 30
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

    def generate_teams_and_stadiums_and_players(self) -> None:

        countries_url: str = (
            'https://raw.githubusercontent.com/annexare/Countries/master/data/'
            'countries.json'
        )
        clubs_url: str = (
            'https://raw.githubusercontent.com/openfootball/football.json/maste'
            'r/2020-21/{}.1.clubs.json'
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

            data: dict[str, list[dict[str, str]]] = response.json()
            obj: dict[str, str]
            for obj in data['clubs']:
                capital: str = countries.get(
                    obj['country'],
                    'Unknown'
                )
                stadium: Stadium
                _: bool
                stadium, _ = Stadium.objects.get_or_create(
                    title=f'{obj["code"]} Stadium',
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

                team = Team.objects.filter(title=obj['name']).first()
                
                MAX_POWER: int = 99
                MIN_POWER: int = 30
                MAX_AGE: int = 40
                MIN_AGE: int = 17
                for _ in range(11):
                    Player.objects.create(
                    status=1,
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
                    ),
                    team=team
            )
    
    def remove_all(self):
        Player.objects.all().delete()
        Team.objects.all().delete()
        Stadium.objects.all().delete()

    def handle(self, *args: Any, **kwargs: Any) -> None:
        start: datetime = datetime.datetime.now()

        # self.remove_all()                
        self.generate_teams_and_stadiums_and_players() 

        print(
            f"Genereated in: {(datetime.datetime.now()-start).total_seconds()}"
        )