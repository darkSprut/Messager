from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Avatar
# Register your models here.


class AvatarInline(admin.StackedInline):
    model = Avatar


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "pk", "created_at", "user_pk"
    inlines = [AvatarInline,]

    def user_pk(self, obj):
        return obj.user.pk


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = "pk", "created_at",


# class UserAdminExtend(UserAdmin):
#     list_display = "pk", "username",
#     inlines = [ProfileInline,]
