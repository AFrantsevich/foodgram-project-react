from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import User
from foodgram.models import Subscribe


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            'is_subscribed'
        )

    def get_is_subscribed(self, *args):
        if self.context['request'].user.is_anonymous:
            return False
        return(any(args[0] == i.author for i in Subscribe.objects.filter(
            user=self.context["request"].user)))


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(
        required=True,
        max_length=150)
    last_name = serializers.CharField(
        required=True,
        max_length=150)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
