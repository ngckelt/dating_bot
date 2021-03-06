# Generated by Django 3.1.8 on 2021-09-05 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0011_auto_20210824_0343'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingQuestionnaires',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('text', models.TextField(verbose_name='Анкета')),
            ],
            options={
                'verbose_name': 'Ожидающая анкета',
                'verbose_name_plural': 'Ожидающие анкеты',
            },
        ),
    ]
