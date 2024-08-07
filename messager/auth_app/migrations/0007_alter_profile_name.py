# Generated by Django 5.0.7 on 2024-08-07 12:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0006_alter_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.TextField(blank=True, default='null', null=True, validators=[django.core.validators.MaxLengthValidator(20, message='значение не может быть больше 20 знаков'), django.core.validators.RegexValidator('admin', inverse_match=True, message='недопустимое значение')]),
        ),
    ]
