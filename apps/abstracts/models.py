from django.db import models

# Django
from django.db import models


class AbstractDateTime(models.Model):
    datetime_created = models.DateTimeField(
        verbose_name='время создания',
        auto_now_add=True
    )
    datetime_updated = models.DateTimeField(
        verbose_name='время обновления',
        auto_now=True
    )
    datetime_deleted = models.DateTimeField(
        verbose_name='время удаления',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
