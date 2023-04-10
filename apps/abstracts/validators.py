# Python
from typing import Any

# DRF
from rest_framework.exceptions import APIException

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str


class APIValidator(APIException):
    """APIValidator."""

    status_code: Any = None

    def __init__(
        self,
        detail: dict[str, Any],
        field: str,
        status_code: str
    ) -> None:

        if status_code is None:
            return

        try:
            self.status_code = settings.STATUS_CODES[status_code]
        except Exception:
            raise ValidationError(
                'StatusCode is unknown'
            )

        if detail is not None:
            self.detail = {
                field: force_str(detail)
            }
        else:
            self.detail = {
                'error': force_str('Server is down')
            }
