from typing import Optional, Any
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from .models import (
    Player,
    Stadium,
    Team,
    Event,
    Result,
    Bet
)


class PlayerAdmin(admin.ModelAdmin):
    """ PlayerAdmin """

    model = Player

    list_display = (
        'status',
        'name',
        'surname',
        'power'
    )

    readonly_fields = (
        'status',
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Player] = None
    ) -> tuple:
        """Get readonly fields."""

        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'team',
            'name',
            'surname',
            'age'
        )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return True

    def has_change_permission(self, request: WSGIRequest, obj: Any = None) -> bool:
        return True

    def has_delete_permission(self, request: WSGIRequest, obj: Any = None) -> bool:
        return True


class TeamAdmin(admin.ModelAdmin):
    """ TeamAdmin """

    model = Team

    list_display = (
        'title',
        'stadium'
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Stadium] = None
    ) -> tuple:
        """ get readonly fields """

        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'title',
            'stadium'
        )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return True

    def has_change_permission(self, request: WSGIRequest, obj: Any = None) -> bool:
        return True

    def has_delete_permission(self, request: WSGIRequest, obj: Any = None) -> bool:
        return True


class StadiumAdmin(admin.ModelAdmin):
    """ StadiumAdmin """

    model = Stadium

    list_display = (
        'title',
        'capacity',
        'city'
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Stadium] = None
    ) -> tuple:
        """ get readonly fields """

        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'title',
            'capacity',
            'city'
        )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return True

    def has_change_permission(self, request: WSGIRequest, obj: Any = None) -> bool:
        return True

    def has_delete_permission(self, request: WSGIRequest, obj: Any = None) -> bool:
        return True


admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium, StadiumAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Event)
admin.site.register(Result)
admin.site.register(Bet)
