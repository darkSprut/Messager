from rest_framework import serializers
from auth_app.models import Profile, Avatar
from .models import Message, Chat
from django.contrib.auth.models import User


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Avatar


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False, read_only=True)

    class Meta:
        fields = "name", "age", "bio", "avatar",
        model = Profile

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.name)
        instance.bio = validated_data.get("bio", instance.name)
        instance.save()
        return instance


class UsersSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = "pk", "username", "profile",


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"

    def create(self, validated_data):
        instance = Message.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("created_at"):
            data["created_at"] = instance.created_at.strftime("%d/%m/%Y %H:%M:%S")
        return data


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = "pk", "users", "messages", "update_at",

