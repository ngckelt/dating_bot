# Generated by Django 3.1.8 on 2021-08-24 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0010_users_known_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='known_users',
            field=models.JSONField(default={'known_users': []}, verbose_name='Известные пользователи'),
        ),
    ]
