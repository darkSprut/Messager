from django.urls import path, include
from .views import ChangeAvatar, GetUser, GetUsers, SendMessage
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    path('change-avatar/', ChangeAvatar.as_view(), name="change-avatar"),
    path('get-change-profile/', GetUser.as_view(), name="get-profile"),
    path('get-users/', GetUsers.as_view(), name="get-users"),
    path('get-users/<int:pk>/', GetUsers.as_view(), name="get-users"),
    path('messages/', SendMessage.as_view(), name="message"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
