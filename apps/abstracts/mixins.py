# Python
from typing import Any

# DRF
from rest_framework.response import Response

# Django
from django.db.models import QuerySet


class ObjectMixin:
    """ObjectMixin."""

    def get_object(
        self,
        queryset: QuerySet[Any],
        obj_id: str
    ) -> Any:
        obj: Any = None
        try:
            obj = queryset.get(id=obj_id)
        except Exception as exc:
            print(f'ERROR.ObjectMixin.get_object: {exc}')
            return None
        else:
            return obj


class ResponseMixin:
    """ResponseMixin."""

    def get_json_response(
        self,
        data: dict[str, Any],
        key_name: str = 'default',
        paginator: Any = None
    ) -> Response:

        if paginator:
            return paginator.get_paginated_response(
                data
            )
        return Response(
            {
                'data': {
                    key_name: data
                }
            }
        )
