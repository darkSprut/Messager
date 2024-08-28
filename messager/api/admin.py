from django.contrib import admin
from .models import Message, Chat, ChatsLog
# Register your models here.


@admin.register(ChatsLog)
class ChatsLogAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "chat", "new_message_count",


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = "pk", "sender", "recipient", "created_at"


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = "pk", "created_at",
