import logging
from django.shortcuts import render, redirect, reverse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from django.views.generic import View, TemplateView
import os
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import caches
from .auth_yandex import AuthenticateYandex
from django.contrib.auth import authenticate, login, logout
from oauthlib import oauth2


class SignView(TemplateView):
    template_name = 'index/sign-in.html'


class IndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'index/index.html', context=context)


class LogOutView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect(reverse("sign-in"))


class SignYandexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        client = oauth2.Client(client_id=os.getenv("YANDEX_CLIENT_ID"))
        code_verifier = client.create_code_verifier(length=50)
        code_challenge = client.create_code_challenge(code_verifier=code_verifier, code_challenge_method="S256")
        request.session["code_verifier"] = code_verifier
        return redirect(
            f'https://oauth.yandex.ru/authorize?response_type=code&client_id={os.getenv("YANDEX_CLIENT_ID")}'
            f'&code_challenge={code_challenge}&code_challenge_method=S256')


class CallbackYandexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        code = request.GET.get('code')
        code_verifier = request.session.get("code_verifier")
        if code and code_verifier:
            scope = self.get_scope(code=code, code_verifier=code_verifier)
            if scope:
                user = self.get_user(scope=scope)
                login(request, user)
                return redirect(reverse("index"))
        return redirect(reverse("sign-in"))

    def get_scope(self, code: int, code_verifier: str) -> dict:
        tokens = AuthenticateYandex.get_tokens_yandex(code, code_verifier)
        scope = AuthenticateYandex.get_scope_yandex(tokens)
        return scope

    def get_user(self, scope: dict) -> User:
        data = scope["payload"]
        pk = data.get("uid")
        username = data.get("login")
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist as err:
            user = User.objects.create_user(pk=pk, username=username)
        return user
