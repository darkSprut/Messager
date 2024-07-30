from django.urls import path, include
from .views import SignInView, SignYandexView, CallbackYandexView, LogOutView

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('yandex/', SignYandexView.as_view(), name='yandex-sign'),
    path('yandex/callback/', CallbackYandexView.as_view(), name='callback-yandex'),
    path('log-out/', LogOutView.as_view(), name='log-out'),
]
