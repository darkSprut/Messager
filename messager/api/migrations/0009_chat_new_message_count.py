# Generated by Django 5.0.7 on 2024-08-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_chat_new_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='new_message_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
