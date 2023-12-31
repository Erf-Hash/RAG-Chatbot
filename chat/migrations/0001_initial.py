# Generated by Django 4.2.7 on 2023-11-26 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pgvector.django


def create_third_party_extension(apps, schema_editor):
    schema_editor.execute("CREATE EXTENSION vector;")


def drop_third_party_extension(apps, schema_editor):
    schema_editor.execute("DROP EXTENSION IF EXISTS vector;")

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_third_party_extension, reverse_code=drop_third_party_extension, atomic=True),
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('title', models.CharField(default=None, max_length=50)),
                ('document_text', models.CharField(max_length=800)),
                ('score', models.IntegerField()),
                ('document_vector', pgvector.django.VectorField(blank=True, dimensions=1536)),
                ('is_active', models.BooleanField()),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=None, max_length=200)),
                ('last_message_date', models.DateTimeField(auto_now=True)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chat.bot')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('comment', models.CharField(blank=True, choices=[('LIKE', 'Like'), ('DISLIKE', 'Dislike')], max_length=10)),
                ('conversation', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.conversation')),
            ],
        ),
    ]
