import logging
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .auth_yandex import AuthenticateYandex
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import ObjectDoesNotExist
import re
from .models import Profile, Avatar


def get_tokens_yandex_middleware(get_response):
    protect_list = [
        reverse('sign-in'), reverse('yandex-sign'), reverse('callback-yandex'),
    ]

    def middleware(request):
        if request.path not in protect_list and not re.search(r'admin', request.path):
            if not request.user.is_authenticated:
                code = request.session.get("code")
                code_verifier = request.session.get("code_verifier")
                tokens = AuthenticateYandex.get_tokens_yandex(code=code, code_verifier=code_verifier)
                request.session["access_token"] = tokens.get("access_token")
                request.session["refresh_token"] = tokens.get("refresh_token")
        response = get_response(request)
        return response
    return middleware


def yandex_auth_middleware(get_response):
    protect_list = [
        reverse('sign-in'), reverse('yandex-sign'), reverse('callback-yandex'),
    ]
    redirect_url = reverse("sign-in")

    def middleware(request):
        if request.path not in protect_list and not re.search(r'admin', request.path):
            if not request.user.is_authenticated:
                everything_all_right = False
                access_token = request.session.get("access_token")
                refresh_token = request.session.get("refresh_token")
                scope = AuthenticateYandex.get_scope_yandex(access_token=access_token, refresh_token=refresh_token)
                if scope:
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
                    request.user = user
                    login(request, user)
                    everything_all_right = True

                if not everything_all_right:
                    return redirect(redirect_url)

        response = get_response(request)
        return response
    return middleware

