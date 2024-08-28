import logging
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .auth_yandex import AuthenticateYandex
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import ObjectDoesNotExist
import re
from .models import Profile, Avatar
from api.models import ChatsLog


class BaseYandexMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.protect_list_url = [
            reverse('auth_app:sign-in'), reverse('auth_app:yandex-sign'), reverse('auth_app:callback-yandex')
        ]

    def check_request(self, request):
        if (request.path not in self.protect_list_url
                and not re.search(r'admin', request.path))\
                and not request.user.is_authenticated:
            return True
        return False


class GetTokensYandexMiddleware(BaseYandexMiddleware):

    def __call__(self, request):
        if self.check_request(request):
            code = request.session.get("code")
            code_verifier = request.session.get("code_verifier")
            tokens = AuthenticateYandex.get_tokens_yandex(code=code, code_verifier=code_verifier)
            request.session["access_token"] = tokens.get("access_token")
            request.session["refresh_token"] = tokens.get("refresh_token")
        response = self.get_response(request)
        return response


class AuthYandexMiddleware(BaseYandexMiddleware):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.redirect_url = reverse("auth_app:sign-in")

    def __call__(self, request):
        if self.check_request(request):
            access_token = request.session.get("access_token")
            refresh_token = request.session.get("refresh_token")
            scope = AuthenticateYandex.get_scope_yandex(access_token=access_token, refresh_token=refresh_token)
            if scope:
                user = self.get_or_create_user(scope=scope)
                request.user = user
                login(request, user)
            else:
                print("redirect")
                return redirect(self.redirect_url)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_or_create_user(scope):
        data = scope.get("payload")
        pk = data.get("uid")
        login_name = data.get("login")
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist as err:
            logging.info(err)
            user = User.objects.create_user(pk=pk, username=login_name)
            profile = Profile.objects.create(user=user)
            Avatar.objects.create(profile=profile)
            ChatsLog.objects.create(user=user)
        return user
