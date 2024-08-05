from django.urls import path, include
from .views import ChangeAvatar, GetUser, GetUsers
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    path('change-avatar/', ChangeAvatar.as_view(), name="change-avatar"),
    path('get-change-user/', GetUser.as_view(), name="get-user"),
    path('get-users/', GetUsers.as_view(), name="get-users"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
