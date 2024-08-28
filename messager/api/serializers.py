from rest_framework import serializers
from auth_app.models import Profile, Avatar
from .models import Message, Chat, ChatsLog
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
    sender = UsersSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = "recipient", "sender", "message", "created_at", "chat",

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
        fields = "pk", "users", "messages", "created_at",


class SimpleChatSerializer(serializers.ModelSerializer):
    users = UsersSerializer(many=True)

    def __init__(self, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs.pop("user_pk"))
        super().__init__(*args, **kwargs)

    class Meta:
        model = Chat
        fields = "pk", "users", "created_at",

    def to_representation(self, instance):
        data = super().to_representation(instance)
        chats_log = ChatsLog.objects.get(chat=instance.pk, user=self.user)
        data["new_message_count"] = chats_log.new_message_count
        data["created_at"] = instance.created_at.strftime("%d/%m/%Y %H:%M:%S")
        return data
