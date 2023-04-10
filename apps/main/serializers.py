# Python
from typing import Any

# DRF
from rest_framework import serializers

# Local
from .models import Player


class TeamSerializer(serializers.Serializer):
    """TeamSerializer."""

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False)

    class Meta:
        model = Player
        fields = (
            'id',
            'title',
        )


class PlayerSerializer(serializers.ModelSerializer):
    """PlayerSerializer."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    power = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=False)
    # status = serializers.SerializerMethodField(
    #     method_name='get_status'
    # )
    # notes = serializers.SerializerMethodField(
    #     method_name='get_notes'
    # )
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Player
        fields = (
            'id',
            'name',
            'surname',
            'power',
            'age',
            # 'status',
            # 'notes',
            'team',
        )


class PlayerDetailSerializer(serializers.ModelSerializer):
    """PlayerSerializer."""
    id = serializers.IntegerField()
    name = serializers.CharField()
    surname = serializers.CharField()
    fullname = serializers.CharField()
    power = serializers.IntegerField()
    status = serializers.SerializerMethodField(
        method_name='get_status'
    )

    class Meta:
        model = Player
        fields = (
            'id',
            'name',
            'surname',
            'fullname',
            'power',
            'age',
            'status'
        )

    def get_status(self, obj: Player):
        return f"{obj.status} | {obj.get_status_display()}"

        
class PlayerCreateSerializer(serializers.ModelSerializer):
    """Player create serializer"""
    name = serializers.CharField()
    surname = serializers.CharField()
    power = serializers.IntegerField()
    age = serializers.IntegerField()

    class Meta:
        model = Player
        fields = (
            'name',
            'surname',
            'power',
            'age'
        )

    def create(self, validated_data: dict[str, Any]) -> Player:
        player: Player = Player.objects.create(
            **validated_data
        )
        return player

