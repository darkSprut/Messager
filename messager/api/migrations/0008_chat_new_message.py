# Generated by Django 5.0.7 on 2024-08-08 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_message_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='new_message',
            field=models.BooleanField(default=False),
        ),
    ]
