# Future
from __future__ import annotations

# Python
from typing import Optional

# Django
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

# Local
from .models import (
    Bet,
    Event,
    Player,
    Result,
    Stadium,
    Team
)


class PlayerAdmin(admin.ModelAdmin):
    """PlayerAdmin."""

    model = Player

    search_fields = (
        'name',
        'surname'
    )
    readonly_fields = ()
    list_filter = (
        'status',
    )
    list_display = (
        'name',
        'surname',
        'power',
        'age'
    )
    ordering = ('-id',)

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Player] = None
    ) -> tuple[str, ...]:
        """Get readonly fields."""

        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'name',
            'surname',
            'age'
        )


class TeamAdmin(admin.ModelAdmin):
    """TeamAdmin."""

    model = Team
    readonly_fields = ()
    list_display = (
        'title',
        'stadium'
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Team] = None
    ) -> tuple[str, ...]:
        """Get readonly fields."""

        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'title',
            'stadium'
        )


class StadiumAdmin(admin.ModelAdmin):
    """StadiumAdmin."""

    model = Stadium
    readonly_fields = ()
    list_display = (
        'title',
        'capacity',
        'city'
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Stadium] = None
    ) -> tuple[str, ...]:
        """Get readonly fields."""

        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'title',
            'capacity',
            'city'
        )


class EventAdmin(admin.ModelAdmin):
    """EventAdmin."""

    model = Event


class ResultAdmin(admin.ModelAdmin):
    """ResultAdmin."""

    model = Result


class BetAdmin(admin.ModelAdmin):
    """BetAdmin."""

    model = Bet


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium, StadiumAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Bet, BetAdmin)
