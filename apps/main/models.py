# Future
from __future__ import annotations

# Python
from typing import Any
import math
from functools import cached_property

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet

from auths.models import Client


class Stadium(models.Model):
    """Stadium."""

    title = models.CharField(
        max_length=25,
        verbose_name='название'
    )
    capacity = models.IntegerField(
        verbose_name='вместимость'
    )
    city = models.CharField(
        max_length=25,
        verbose_name='город'
    )

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'стадион'
        verbose_name_plural = 'стадионы'

    def __str__(self) -> str:
        return self.title


class Team(models.Model):
    """Team."""
    
    MAX_PLAYERS: int = 11

    title = models.CharField(
        max_length=25,
        verbose_name='название'
    )
    stadium = models.ForeignKey(
        Stadium,
        on_delete=models.RESTRICT,
        verbose_name='стадион'
    )

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'команда'
        verbose_name_plural = 'команды'

    def __str__(self) -> str:
        return self.title

    @cached_property
    def power(self) -> int | float:
        total: int | float = 0
        player: Player
        for player in self.players.all():
            total += player.power
        return math.ceil(total / self.MAX_PLAYERS)


class PlayerManager(models.QuerySet):

    def get_free_agents(self) -> QuerySet['Player']:
        return self.filter(
            status=Player.STATUS_FREE_AGENT
        )

    def get_team_members(self) -> QuerySet['Player']:
        return self.filter(
            status=Player.STATUS_TEAM_MEMBER
        )

    def get_young_players(self) -> QuerySet['Player']:
        return self.filter(
            status=Player.STATUS_TEAM_MEMBER,
            age__lt=Player.ADULT_TEAM_MIN_AGE,
            power__lte=Player.ADULT_TEAM_MIN_POWER
        )

    def get_players_with_teams(self) -> QuerySet['Player']:
        return self.filter(
            status=Player.STATUS_TEAM_MEMBER
        ).exclude(
            team=None
        )


class Player(models.Model):
    """Player."""
    ADULT_TEAM_MIN_AGE: int = 17
    ADULT_TEAM_MAX_AGE: int = 45
    ADULT_TEAM_MIN_POWER: int = 30
    STATUS_FREE_AGENT: int = 0
    STATUS_TEAM_MEMBER: int = 1
    STATUS_RETIRED: int = 2
    STATUSES: tuple[tuple[int, str], ...] = (
        (STATUS_FREE_AGENT, 'Свободный агент'),
        (STATUS_TEAM_MEMBER, 'Состоит в команде'),
        (STATUS_RETIRED, 'Завершил карьеру')
    )
    name: str = models.CharField(
        max_length=25,
        verbose_name='имя'
    )
    surname: str = models.CharField(
        max_length=25,
        verbose_name='фамилия'
    )
    power: int = models.PositiveSmallIntegerField(
        verbose_name='сила'
    )
    age: int = models.PositiveSmallIntegerField(
        verbose_name='возраст'
    )
    status: int = models.PositiveSmallIntegerField(
        choices=STATUSES,
        default=STATUS_FREE_AGENT,
        verbose_name='статус'
    )
    team: Team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name='players',
        verbose_name='команда'
    )

    objects = PlayerManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'

    def clean(self) -> None:
        if (
            self.age < self.ADULT_TEAM_MIN_AGE
        ) or (
            self.age >= self.ADULT_TEAM_MAX_AGE
        ):
            raise ValidationError('Player age invalid')

        if self.power < self.ADULT_TEAM_MIN_POWER:
            raise ValidationError('Player power invalid')

    def save(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        self.status = self.STATUS_FREE_AGENT
        self.save(update_fields=('status',))
        # super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name} {self.surname} | {self.power}'

    @property
    def fullname(self) -> str:
        return f'{self.name} {self.surname}'

    def free(self) -> None:
        self.status = self.STATUS_FREE_AGENT
        self.save(update_fields=('status',))

    def retire(self) -> None:
        self.status = self.STATUS_RETIRED
        self.save(update_fields=('status',))


class Result(models.Model):
    """Result."""

    won_team_id: int = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='кто выйграл'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'результат'
        verbose_name_plural = 'результаты'

    def __str__(self) -> str:
        return f'Выграла команда с ID: {self.won_team_id}'


class Event(models.Model):
    """Event."""

    STATUS_FUTURE: int = 0
    STATUS_ONGOING: int = 1
    STATUS_PAST: int = 2
    STATUSES: tuple[tuple[int, str], ...] = (
        (STATUS_FUTURE, 'Состоится'),
        (STATUS_ONGOING, 'В процессе'),
        (STATUS_PAST, 'Состоялось')
    )
    status: int = models.PositiveSmallIntegerField(
        choices=STATUSES,
        default=STATUS_FUTURE,
        verbose_name='статус'
    )
    team_1: Team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        related_name='team_1',
        verbose_name='команда 1'
    )
    team_2: Team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        related_name='team_2',
        verbose_name='команда 2'
    )
    result: Result = models.OneToOneField(
        Result,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='результат'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'событие'
        verbose_name_plural = 'события'

    def __str__(self) -> str:
        return (
            f'{self.get_status_display()} | '
            f'{self.team_1.title} VS '
            f'{self.team_2.title}'
        )

    @cached_property
    def who_won(self) -> Team:
        if self.result.won_team_id == self.team_1.id:
            return self.team_1
        return self.team_2


class Bet(models.Model):
    """Bet."""

    client: Client = models.ForeignKey(
        Client,
        on_delete=models.RESTRICT,
        verbose_name='клиент'
    )
    event: Event = models.ForeignKey(
        Event,
        on_delete=models.RESTRICT,
        verbose_name='событие'
    )
    amount: int = models.PositiveIntegerField(
        verbose_name='сумма'
    )
    chosen_team_id: int = models.PositiveSmallIntegerField(
        verbose_name='выбранная команда'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'ставка'
        verbose_name_plural = 'ставки'

    def __str__(self) -> str:
        return f'{self.client.email} | {self.amount}'
