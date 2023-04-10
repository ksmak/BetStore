# Python
import math
import random

# Django
from django.test import TestCase

# Local
from .models import (
    Player,
    Stadium,
    Team
)


class PlayerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        stadium = Stadium.objects.create(
            title='Stadium 1',
            capacity=80000,
            city='Milan'
        )
        team = Team.objects.create(
            title='Team 1',
            stadium=stadium
        )
        for _ in range(Team.MAX_PLAYERS):
            power = random.randrange(50, 90, 5)
            Player.objects.create(
                name='Name',
                surname='Surname',
                power=power,
                status=Player.STATUS_RETIRED,
                age=20,
                team=team
            )

    def setUp(self):
        self.player = Player.objects.create(
            name='name',
            surname='surname',
            power=Player.ADULT_TEAM_MIN_POWER,
            age=Player.ADULT_TEAM_MIN_AGE
        )
        self.player2 = Player.objects.create(
            name='name 2',
            surname='surname 2',
            power=Player.ADULT_TEAM_MIN_POWER,
            age=Player.ADULT_TEAM_MIN_AGE
        )
        self.stadium = Stadium.objects.create(
            title='Stadium 2',
            capacity=80000,
            city='Milan'
        )
        self.team = Team.objects.create(
            title='Team 2',
            stadium=self.stadium
        )
        self.stadium2 = Stadium.objects.create(
            title='Stadium 3',
            capacity=80000,
            city='Milan'
        )

    def test_player_creation(self):
        self.assertEqual(self.player.id, 12)
        self.assertEqual(self.player2.id, 13)

    def test_player_fullname(self):
        expected_fullname = f'{self.player.name} {self.player.surname}'
        self.assertEqual(self.player.fullname, expected_fullname)

    def test_player_free(self):
        self.assertEqual(self.player.status, Player.STATUS_FREE_AGENT)
        self.player.free()
        self.assertEqual(self.player.status, Player.STATUS_FREE_AGENT)

    def test_player_retire(self):
        self.assertEqual(self.player.status, Player.STATUS_FREE_AGENT)
        self.player.retire()
        self.assertEqual(self.player.status, Player.STATUS_RETIRED)

    def test_team(self):
        self.assertEqual(self.team.stadium.id, self.stadium.id)
        self.team.stadium = self.stadium2
        self.assertEqual(self.team.stadium.id, self.stadium2.id)

    def test_team_power(self):
        team = Team.objects.get(id=1)
        total = 0
        for player in team.players.all():
            total += player.power

        power = math.ceil(total / Team.MAX_PLAYERS)
        self.assertEqual(team.power, power)

    def test_players_delete(self):
        players = Player.objects.filter(
            status=Player.STATUS_RETIRED
        )
        for player in players:
            player.delete()

        self.assertTrue(
            Player.STATUS_RETIRED not in [i.status for i in players]
        )
