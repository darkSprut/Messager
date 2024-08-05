from django.urls import path, include
from .views import SignInView, SignYandexView, CallbackYandexView, LogOutView

app_name = 'auth_app'

yandex_urlpatterns = [
    path('', SignYandexView.as_view(), name='yandex-sign'),
    path('callback/', CallbackYandexView.as_view(), name='callback-yandex'),
]

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('log-out/', LogOutView.as_view(), name='log-out'),
    path('yandex/', include(yandex_urlpatterns)),
]
