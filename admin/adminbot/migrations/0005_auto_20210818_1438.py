# Generated by Django 3.1.8 on 2021-08-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0004_auto_20210818_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchquestions',
            name='question_id',
            field=models.CharField(blank=True, editable=False, max_length=20, verbose_name='ID вопроса'),
        ),
        migrations.AddField(
            model_name='userquestions',
            name='question_id',
            field=models.CharField(blank=True, editable=False, max_length=20, verbose_name='ID вопроса'),
        ),
    ]
