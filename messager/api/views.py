from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProfileSerializer, UsersSerializer
from django.contrib.auth.models import User
from auth_app.models import Profile, Avatar
from rest_framework import status
from django.db.models import ObjectDoesNotExist

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
        if username:
            users = User.objects.filter(username__icontains=username)
        else:
            users = User.objects.all()
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
