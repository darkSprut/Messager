from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name="chats", null=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'chat_No{self.pk}'


class ChatsLog(models.Model):
    user = models.ForeignKey(User, related_name="chats_log", on_delete=models.CASCADE, null=False)
    chat = models.ForeignKey(Chat, related_name="chats_log", on_delete=models.CASCADE, null=True)
    new_message_count = models.PositiveSmallIntegerField(default=0)


class Message(models.Model):
    recipient = models.ForeignKey(User, related_name="received_message", on_delete=models.SET("deleted"))
    sender = models.ForeignKey(User, related_name="sent_message", on_delete=models.SET("deleted"))
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", null=True)

    class Meta:
        ordering = ["created_at"]
