from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        BASIC = "BASIC"
        PREMIUM = "PREMIUM"

    role = models.CharField(max_length=10, choices=Role.choices)


class Bot(models.Model):
    content = models.CharField(max_length=800)


class Message(models.Model):
    class CommentChoices(models.TextChoices):
        LIKE = "LIKE"
        DISLIKE = "DISLIKE"

    message = models.CharField(max_length=100)
    comment = models.CharField(max_length=10, choices=CommentChoices.choices)


class Conversation(models.Model):
    messages = models.ForeignKey(
        Message, on_delete=models.CASCADE, default=None, null=True
    )
