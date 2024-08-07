from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProfileSerializer, UsersSerializer, MessageSerializer, ChatSerializer
from django.contrib.auth.models import User
from auth_app.models import Profile, Avatar
from rest_framework import status
from django.db.models import ObjectDoesNotExist
from .models import Chat
from django.db.models import Q

# Create your views here.


class GetUser(APIView):

    def get(self, request: Request, *args, **kwargs):
        serialized = UsersSerializer(request.user, many=False)
        return Response(serialized.data)

    def put(self, request: Request) -> Response:
        user = request.user
        profile = Profile.objects.get(user=user)
        serialize = ProfileSerializer(data=request.data)
        if serialize.is_valid():
            serialize.update(profile, serialize.validated_data)
            return Response()
        else:
            return Response(data=serialize.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class GetUsers(APIView):

    def get(self, request: Request, *args, **kwargs) -> Response:
        username = request.GET.get("username")
        pk = kwargs.get("pk")
        if username:
            users = User.objects.filter(username__icontains=username).exclude(username=request.user.username)
            serialized = UsersSerializer(users, many=True)

        elif pk:
            user = get_object_or_404(User, pk=pk)
            serialized = UsersSerializer(user, many=False)
        else:
            users = User.objects.all().exclude(pk=request.user.pk)
            serialized = UsersSerializer(users, many=True)
        return Response(serialized.data)


class ChangeAvatar(APIView):

    def post(self, request: Request) -> Response:
        if request.FILES:
            user = request.user
            file = request.FILES.get("avatar_form")
            profile = Profile.objects.get(user=user)
            try:
                avatar = Avatar.objects.get(profile__user=user)
            except ObjectDoesNotExist as err:
                avatar = Avatar.objects.create(image=file, profile=profile)
            else:
                avatar.delete()
                Avatar.objects.create(image=file, profile=profile)
        return Response()


class SendMessage(APIView):

    def get(self, request: Request, *args, **kwargs) -> Response:
        recipient = get_object_or_404(User, pk=request.query_params.get("recipient"))
        try:
            chat = Chat.objects.get(Q(users__in=[recipient]) and Q(users__in=[request.user]))
        except ObjectDoesNotExist as err:
            return Response()
        else:
            serialize = ChatSerializer(chat, many=False)
            return Response(serialize.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        request.data["sender"] = request.user.pk
        serialize = MessageSerializer(data=request.data, many=False)
        if serialize.is_valid():
            message = serialize.create(serialize.validated_data)
            self.add_message_to_chat(request=request, message=message)
            return Response(serialize.data)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def add_message_to_chat(self, request: Request, message):
        recipient = get_object_or_404(User, pk=request.data.get("recipient"))
        try:
            chat = Chat.objects.get(Q(users__in=[recipient]) and Q(users__in=[request.user]))
        except ObjectDoesNotExist as err:
            chat = Chat.objects.create()
            chat.users.add(recipient.pk)
            chat.users.add(request.user.pk)
        finally:
            chat.messages.add(message)
            # вызываем явно метод save, чтобы обновить временную метку
            chat.save()
