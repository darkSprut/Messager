# Generated by Django 5.0.7 on 2024-08-07 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='text',
            new_name='message',
        ),
    ]
