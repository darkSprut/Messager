from django.urls import path, include
from .views import SignView, SignYandexView, IndexView, CallbackYandexView, LogOutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sign-in/', SignView.as_view(), name='sign-in'),
    path('log-out/', LogOutView.as_view(), name='log-out'),
    path('yandex/', SignYandexView.as_view(), name='yandex-sign'),
    path('yandex/callback/', CallbackYandexView.as_view(), name='callback-yandex'),
]
