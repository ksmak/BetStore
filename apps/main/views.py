# Python
from typing import (
    Any,
    Optional
)

# DRF
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# Django
from django.db.models.query import QuerySet

# First party
from abstracts.decorators import performance_counter
from abstracts.mixins import (
    ObjectMixin,
    ResponseMixin
)
from abstracts.paginators import (
    AbstractLimitOffsetPagination,
    AbstractPageNumberPaginator,
    MyPagination
)
# from abstracts.validators import APIValidator
from main.permissions import MainPermission

# Local
from .models import Player
from .serializers import (
    PlayerCreateSerializer,
    PlayerSerializer
)


class MainViewSet(ResponseMixin, ObjectMixin, ViewSet):
    """MainViewSet."""

    permission_classes: tuple[Any, ...] = (
        MainPermission,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    queryset = Player.objects.all()

    @action(
        methods=['get'],
        detail=False,
        url_path='no-pagination',
        permission_classes=(AllowAny,)
    )
    def no_pagination(self, request: Request) -> Response:
        players: QuerySet[Player] = self.queryset.all()
        serializer: PlayerSerializer = \
            PlayerSerializer(
                players,
                many=True
            )
        return self.get_json_response(serializer.data, 'players')

    @action(
        methods=['get'],
        detail=False,
        url_path='pagination-type-1',
        permission_classes=(AllowAny,)
    )
    def pagination_type_1(self, request: Request) -> Response:

        paginator: AbstractPageNumberPaginator = \
            self.pagination_class()

        objects: list = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: PlayerSerializer = \
            PlayerSerializer(
                objects,
                many=True
            )
        return self.get_json_response(
            serializer.data,
            'players',
            paginator
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='pagination-type-2',
        permission_classes=(AllowAny,)
    )
    def pagination_type_2(self, request: Request) -> Response:

        paginator: AbstractLimitOffsetPagination = \
            AbstractLimitOffsetPagination()

        objects: list = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: PlayerSerializer = \
            PlayerSerializer(
                objects,
                many=True
            )
        return self.get_json_response(
            serializer.data,
            'players',
            paginator
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='custom-pagination',
        permission_classes=(AllowAny,)
    )
    def custom_pagination(self, request: Request) -> Response:

        paginator: MyPagination = \
            MyPagination()

        objects: list = paginator.paginate_queryset(
            self.queryset,
            request
        )
        serializer: PlayerSerializer = \
            PlayerSerializer(
                objects,
                many=True
            )
        return self.get_json_response(
            serializer.data,
            'players',
            paginator
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='get-players',
        permission_classes=(AllowAny,)
    )
    def get_players(self, request: Request) -> Response:
        """GET method."""

        players: QuerySet[Player] = \
            self.queryset.all()[:100]

        serializer: PlayerSerializer = \
            PlayerSerializer(
                players,
                many=True
            )
        return self.get_json_response(serializer.data, 'players')

    @performance_counter
    def list(self, request: Request) -> Response:
        """GET method."""

        players: QuerySet[Player] = self.queryset.all()[:10]
        serializer: PlayerSerializer = \
            PlayerSerializer(
                players,
                many=True
            )
        return self.get_json_response(serializer.data, 'players')

    def retrieve(self, request: Request, pk: str) -> Response:
        """GET method."""

        player: Optional[Player] = self.get_object(
            self.queryset,
            pk
        )
        if not player:
            return Response(
                {
                    'data': {
                        'error': 'No such player'
                    }
                }
            )
        return self.get_json_response(
            {
                'name': player.name,
                'surname': player.surname,
                'power': player.power,
                'age': player.age
            }
        )

    def create(self, request: Request) -> Response:
        """POST method."""

        serializer: PlayerCreateSerializer = \
            PlayerCreateSerializer(
                data=request.data
            )
        if not serializer.is_valid():
            return Response(
                {
                    'data': serializer.errors
                }
            )
        player: Player = serializer.save()
        return self.get_json_response(player.fullname, 'players')

    def update(self, request: Request, pk: str) -> Response:
        """POST method."""

        player: Optional[Player] = self.get_object(
            self.queryset,
            pk
        )
        if not player:
            return Response(
                {
                    'data': {
                        'error': 'No such player'
                    }
                }
            )
        serializer: PlayerSerializer = PlayerSerializer(
            player,
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                {
                    'data': {
                        'error': serializer.errors
                    }
                }
            )
        serializer.save()
        return self.get_json_response('Updated', 'success')

    def partial_update(self, request: Request, pk: str) -> Response:
        """POST method."""

        player: Optional[Player] = self.get_object(
            self.queryset,
            pk
        )
        if not player:
            return Response(
                {
                    'data': {
                        'error': 'No such player'
                    }
                }
            )
        serializer: PlayerSerializer = PlayerSerializer(
            player,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(
                {
                    'data': {
                        'error': serializer.errors
                    }
                }
            )
        serializer.save()
        return self.get_json_response('Partially Updated', 'success')

    def destroy(self, request: Request, pk: str) -> Response:
        """DELETE method."""

        player: Optional[Player] = self.get_object(
            self.queryset,
            pk
        )
        if not player:
            return Response(
                {
                    'data': {
                        'error': 'No such player'
                    }
                }
            )
        player.delete()
        return self.get_json_response('Player deleted', 'error')
