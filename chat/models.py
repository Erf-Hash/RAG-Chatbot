from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        BASIC = "BASIC"
        PREMIUM = "PREMIUM"

    role = models.CharField(max_length=10, choices=Role.choices)


class Bot(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=50, default=None)
    last_message_date = models.DateTimeField()
    content = models.CharField(max_length=800)


class Message(models.Model):
    class CommentChoices(models.TextChoices):
        LIKE = "LIKE"
        DISLIKE = "DISLIKE"

    message = models.CharField(max_length=100)
    comment = models.CharField(max_length=10, choices=CommentChoices.choices, blank=True)


class Conversation(models.Model):
    title = models.CharField(max_length=50, default=None)
    messages = models.ForeignKey(
        Message, on_delete=models.CASCADE, default=None, null=True
    )
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING)
