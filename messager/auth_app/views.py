import logging
import time

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


class SignInView(TemplateView):
    template_name = 'auth_app/sign-in.html'


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
        context = {

        }
        code = request.GET.get('code')
        request.session["code"] = code
        return render(request=request, template_name='auth_app/sign-in-callback.html', context=context)


class LogOutView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect(reverse("sign-in"))
