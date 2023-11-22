from django.db import models
from django.contrib.auth.models import AbstractUser
from pgvector.django import VectorField
from .utilities import get_embedding


class Bot(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=50, default=None)
    document_text = models.CharField(max_length=800)
    document_vector = VectorField(dimensions=1536, blank=True)

    def save(self, *args, **kwargs):
        self.document_vector = get_embedding(self.document_text)
        super().save(*args, **kwargs)
    



class Conversation(models.Model):
    title = models.CharField(max_length=50, default=None, blank=True)
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING)
    last_message_date = models.DateTimeField(auto_now=True)



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
