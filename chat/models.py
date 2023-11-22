from django.db import models
from django.contrib.auth.models import AbstractUser
from pgvector.django import VectorField
from .utilities import get_embedding


class User(AbstractUser):
    class Role(models.TextChoices):
        BASIC = "BASIC"
        PREMIUM = "PREMIUM"

    role = models.CharField(max_length=10, choices=Role.choices)


class Bot(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=50, default=None)
    last_message_date = models.DateTimeField(blank=True)
    document_text = models.CharField(max_length=800)
    document_vector = VectorField(dimensions=1536, blank=True)

    @classmethod
    def create(cls, name, title, last_message_date, document_text):
        document_vector = get_embedding(document_text)
        print("hello")
        return cls(
            name=name,
            title=title,
            last_message_date=last_message_date,
            document_text=document_text,
            document_vector=document_vector,
        )


class Conversation(models.Model):
    title = models.CharField(max_length=50, default=None)
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING)


class Message(models.Model):
    class CommentChoices(models.TextChoices):
        LIKE = "LIKE"
        DISLIKE = "DISLIKE"

    message = models.CharField(max_length=100)
    comment = models.CharField(
        max_length=10, choices=CommentChoices.choices, blank=True
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, default=None, null=True
    )
