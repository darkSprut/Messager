from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name="chats", null=True)
    update_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    recipient = models.ForeignKey(User, related_name="received_message", on_delete=models.SET("deleted"))
    sender = models.ForeignKey(User, related_name="sent_message", on_delete=models.SET("deleted"))
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", null=True)

    class Meta:
        ordering = ["created_at"]
