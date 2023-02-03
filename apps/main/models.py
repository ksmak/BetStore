# Future
from __future__ import annotations

# Python
from typing import Any
from functools import cached_property

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet

# First party
from auths.models import Client


class Team(models.Model):
    """Team."""

    title = models.CharField(
        verbose_name='название',
        max_length=25
    )

    stadium = models.ForeignKey(
        verbose_name='стадион команды',
        to='Stadium',
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'команда'
        verbose_name_plural = 'команды'

    def __str__(self) -> str:
        return self.title


class PlayerManager(models.Manager):
    """PlayerManager."""

    def get_free_agents(self) -> QuerySet['Player']:
        """ Метод для получения всех игроков со статусом Свободный агент """
        return self.filter(
            status=Player.FREE_AGENT
        )

    def get_team_members(self) -> QuerySet['Player']:
        """ Метод для получения всех игроков со статусом Состоит в команде"""
        return self.filter(
            status=Player.STATUS_TEAM_MEMBER
        )

    def get_young_players(self) -> QuerySet['Player']:
        """
            Метод для получения всех молодых игроков не старше 21,
            состоящих в команде и имеющих силу не меньше 50
        """
        return self.filter(
            status=Player.TEAM_MEMBER,
            age__lt=Player.MIN_AGE_FOR_ADULT_TEAM,
            power__lte=Player.MIN_POWER_FOR_ADULT_TEAM
        )


class Player(models.Model):
    """Player."""

    FREE_AGENT: int = 0
    TEAM_MEMBER: int = 1
    PLAYER_STATUSES: tuple[tuple[int, str], ...] = (
        (FREE_AGENT, 'Свободный агент'),
        (TEAM_MEMBER, 'Состоит в команде')
    )

    MIN_AGE_FOR_ADULT_TEAM: int = 17
    MAX_AGE_FOR_ADULT_TEAM: int = 50
    MIN_POWER_FOR_ADULT_TEAM: int = 30

    status = models.SmallIntegerField(
        choices=PLAYER_STATUSES,
        default=FREE_AGENT,
        verbose_name='статус'
    )

    name = models.CharField(
        max_length=25,
        verbose_name='имя'
    )

    surname = models.CharField(
        max_length=25,
        verbose_name='фамилия'
    )

    power = models.IntegerField(
        verbose_name='сила'
    )

    age = models.IntegerField(
        verbose_name='возраст'
    )

    team = models.ForeignKey(
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

    def __str__(self) -> str:
        return f'{self.name} {self.surname} | {self.power}'

    def clean(self) -> None:
        """
            Метод проверки правильности заполнения
        """
        if (self.age < self.MIN_AGE_FOR_ADULT_TEAM) or (self.age >= self.MAX_AGE_FOR_ADULT_TEAM):
            raise ValidationError('Player age invalid')

        if self.power < self.MIN_POWER_FOR_ADULT_TEAM:
            raise ValidationError('Player power invalid')

    def save(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """ Переопределенный метод сохранения """
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """ Переопределенный метод удаления """
        # self.status = self.FREE_AGENT
        # self.save(
        #     update_fields=('status',)
        # )
        super().delete(*args, **kwargs)


class Stadium(models.Model):
    """Stadium."""

    title = models.CharField(
        max_length=40,
        verbose_name='название стадиона'
    )

    capacity = models.CharField(
        max_length=50,
        verbose_name='место расположения',
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=50,
        verbose_name='город',
        null=True,
        blank=True
    )

    class Meta:
        ordering = (
            'title',
        )
        verbose_name = 'стадион'
        verbose_name_plural = 'стадионы'

    def __str__(self) -> str:
        return f'{self.title}'


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
