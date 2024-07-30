from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserSerializers, ProfileSimpleSerializer, ErrorsSerializer
from auth_app.models import Profile, Avatar
from rest_framework import status
from django.views.generic import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
# Create your views here.


class ProfileAPIView(APIView):

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        serialised = ProfileSerializer(profile)
        return Response(serialised.data)

    def post(self, request: Request) -> Response:
        user = request.user
        serialize = ProfileSimpleSerializer(data=request.data)
        if serialize.is_valid():
            profile = Profile.objects.filter(user=user)
            profile.update(**serialize.validated_data)
            return Response()
        else:
            serialize_errors_data = ErrorsSerializer(serialize.errors).data()
            return Response(data=serialize_errors_data, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangeAvatarView(View):

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.FILES:
            user = request.user
            file = request.FILES.get("avatar_form")
            profile = Profile.objects.get(user=user)
            avatar = Avatar.objects.get(profile=profile)
            avatar.delete()
            Avatar.objects.create(image=file, profile=profile)
        return HttpResponse()
