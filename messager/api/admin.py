from django.contrib import admin
from .models import Message, Chat
# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = "pk", "sender", "recipient", "created_at"


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = "pk", "update_at",
