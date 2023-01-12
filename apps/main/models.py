# Future
from __future__ import annotations

# Python modules
from typing import Any

# Django modules
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

# Project modules
from django.db import models


class Team(models.Model):
    """ Модель Команда """

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
    """ Менеджер модели Игрок """

    def get_free_agents(self) -> QuerySet['Player']:
        """ Метод для получения всех игроков со статусом Свободный агент """
        return self.filter(
            status=Player.FREE_AGENT
        )

    def get_team_members(self) -> QuerySet['Player']:
        """ Метод для получения всех игроков со статусом Состоит в команде"""
        return self.filter(
            status=Player.TEAM_MEMBER
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
    """ Модель Игрок """

    FREE_AGENT: int = 0
    TEAM_MEMBER: int = 1
    PLAYER_STATUSES: tuple[tuple[int, str], ...] = (
        (FREE_AGENT, 'Свободный агент'),
        (TEAM_MEMBER, 'Состоит в команде')
    )

    MIN_AGE_FOR_ADULT_TEAM: int = 21
    MIN_POWER_FOR_ADULT_TEAM: int = 50

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
        verbose_name='команда',
        null=True,
        blank=True,
        related_name='players'
    )

    objects = PlayerManager()

    class Meta:
        ordering = (
            '-power',
        )
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'

    def __str__(self) -> str:
        return f'{self.name} {self.surname} | {self.power}'

    def clean(self) -> None:
        """
            Метод проверки правильности заполнения
        """
        if (self.age < 17) or (self.age >= 50):
            raise ValidationError('Player age invalid')
        if self.power < 50:
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
    """ Модель Стадион """

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
