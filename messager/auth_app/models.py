from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, RegexValidator
from django.contrib.auth.models import User
from .utils import avatar_upload
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=False)
    name = models.TextField(default='null', null=True, blank=True, validators=[
        MaxLengthValidator(20, message="значение не может быть больше 20 знаков"),
        RegexValidator('admin', inverse_match=True, message="недопустимое значение")
    ])
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0, message="значение не может быть меньше 0"),
                    MaxValueValidator(100, message="значение не может быть больше 100")],
        default=0, blank=True, null=True)
    bio = models.TextField(default='null', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Avatar(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="avatar", null=True)
    image = models.ImageField(upload_to=avatar_upload, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    alt = models.CharField(max_length=20, default="avatar")
