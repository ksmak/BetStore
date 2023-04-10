# Python
from typing import Any

# DRF
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class MainPermission(BasePermission):
    """MainPermission."""

    def has_permission(
        self,
        request: Request,
        view: Any
    ) -> bool:
        user: bool = (
            request.user and request.user.is_active
        )
        superuser: bool = user and (
            request.user.is_staff and
            request.user.is_superuser
        )
        if view.action in (
            'list',
            'retrieve'
        ):
            return user

        if view.action in (
            'create',
            'update',
            'partial_update',
            'destroy',
        ):
            return superuser
