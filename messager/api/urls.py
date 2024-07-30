from django.urls import path, include
from .views import ProfileAPIView, ChangeAvatarView

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name="api-profile"),
    path('change-avatar/', ChangeAvatarView.as_view(), name="change-avatar"),
]
